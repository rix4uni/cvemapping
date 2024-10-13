# CVE-2017-0144---EtneralBlue-MS17-010-Remote-Code-Execution

The attacker machine is Kali Linux and Windows Server 2008 R2 as the target machine.

Import the windows 2008 R2 Server from the given https://drive.google.com/drive/folders/146ViggeQl0pSpzotcAhpd3h9UP7fFOxJ?usp=sharing into your virtual box and set the network to bridge adaptor.

**Follow the below steps inorder to exploit the vulnerability.**

<b>Step 1:</b> Checking the attacker machine Ip address and it has been confirmed as 192.168.29.58.
![3](https://user-images.githubusercontent.com/80981816/111834375-85635780-8919-11eb-91e8-c8f1977265ad.png)





<b>Step 2:</b> Using the Advanced IP Scanner we are scanning the entire network to find the Windows Server 2008 R2.
  ![4](https://user-images.githubusercontent.com/80981816/111834382-898f7500-8919-11eb-807c-bb9e3a8bc641.png)


<b>Step 3:</b> checking whether the target machine is reachable or not using a ping command and it has been confirmed the target system is reachable.
 ![5](https://user-images.githubusercontent.com/80981816/111834390-8dbb9280-8919-11eb-92fa-e8d36ead70be.png)


<b>Step 4:</b> With the help of Nmap tool we are checking the service and version detection using   -sC / -sV.
 ![6](https://user-images.githubusercontent.com/80981816/111834403-914f1980-8919-11eb-816d-065efb726b25.png)


<b>Step 5:</b> We can use Nmap as an alternative to the Metasploit scanner to discover if a target is vulnerable to EternalBlue. The Nmap Scripting Engine is a powerful feature of the core tool that allows all kinds of scripts to run against a target.
Here, we'll be using the smb-vuln-ms17-010 script to check for the vulnerability. We can specify a single script to run with the --script option, along with our target's IP address.
Nmap will start running and shouldn't take too long since we are only running one script. At the bottom of the output, we'll find the results.
 ![7](https://user-images.githubusercontent.com/80981816/111834413-957b3700-8919-11eb-872e-34781c033267.png)


<b>Step 6:</b> Use the search command within Metasploit to locate a suitable module to use.
 ![8](https://user-images.githubusercontent.com/80981816/111834427-99a75480-8919-11eb-8d96-775f22ac7b74.png)
Once we have determined that our target is indeed vulnerable to EternalBlue, we can use the following exploit module from the search we just did.

<b>Step 7:</b> We can take a look at the current settings with the show options command. Then set rhosts IP which is fixing the target IP to attack. That should be everything, so the only thing left to do is launch the exploit. Use the Exploit command to fire it off.
 ![9](https://user-images.githubusercontent.com/80981816/111834446-a035cc00-8919-11eb-9f71-cecb2845a420.png)


<b>Step 8:</b> We see a few things happen here, like the SMB connection being established and the exploit packet being sent. At last, we see a "WIN" session is opened.
 ![10](https://user-images.githubusercontent.com/80981816/111834460-a461e980-8919-11eb-95b5-70396862b962.png)
 
 
<b>Step 9:</b> We can verify that we have compromised the target by running commands such as ipconfig to obtain the target IP address.
![11](https://user-images.githubusercontent.com/80981816/111834480-a88e0700-8919-11eb-8ee6-34b1212f2111.png) 


<b>Step 10:</b> “Whoami” prints the effective username of the current user when invoked and net users will show you the user accounts on the computer.
 ![12](https://user-images.githubusercontent.com/80981816/111834343-7a102c00-8919-11eb-81c4-58bebfd9ecba.png)


<b>Step 11:</b> Creating a user zack and adding the user to local group Administrator and Remote Desktop users.
 ![13](https://user-images.githubusercontent.com/80981816/111834330-7381b480-8919-11eb-863b-1bb8eaf32d36.png)


<b>Step 12:</b> Checking the information of the user account zack.
 ![14](https://user-images.githubusercontent.com/80981816/111834311-6bc21000-8919-11eb-8508-f9adb80ed312.png)


<b>Step 13:</b> Connecting the target machine using the created user and password through Remote Desktop Connection.
 ![15](https://user-images.githubusercontent.com/80981816/111834295-65339880-8919-11eb-96c0-49a5f14e21dc.png)


<b>Step 14:</b> Successfully logged into the target system using the created user accounts.
 ![16](https://user-images.githubusercontent.com/80981816/111833469-3963e300-8918-11eb-9c2c-e20a64eeab5a.png)



**Follow the below steps inorder to patch the vulnerability.**
 
step 1: download the patch file from https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2017/ms17-010?redirectedfrom=MSDN and install in the affected machine 
![patch 1](https://user-images.githubusercontent.com/80981816/111836797-e04a7e00-891c-11eb-9a5e-9e69e9d65bd9.png)

Step 2: once patch is installed check with the metasploit auxilary module

**Steps to run Auxilary module:**

(i)use auxilary/scanner/smb/smb_ms17_010

(ii)set rhosts 192.168.29.162

(iii)run

![patchq](https://user-images.githubusercontent.com/80981816/111837000-3b7c7080-891d-11eb-82ae-614bb4ec4a88.png)
