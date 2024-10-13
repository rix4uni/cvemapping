# CVE-2016-8610 PoC
CVE-2016-8610 (SSL Death Alert) PoC

Usage:

python ssl-death-alert.py DOMAIN/IP PORT PROTOCOL-VERSION(SSLv3, TLS1.0, TLS1.1, TLS1.2) NUMBER-OF-ALERTS(1000) THREADS(50)

python ssl-death-alert.py test.tdl 443 TLS1.2 1000 50

More info:

http://security.360.cn/cve/CVE-2016-8610/

https://securingtomorrow.mcafee.com/mcafee-labs/ssl-death-alert-cve-2016-8610-can-cause-denial-of-service-to-openssl-servers/
