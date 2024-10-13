# CVE-2017-1000028
POC&amp;EXP for GlassFish&lt;4.1.1(not including 4.1.1).

Param:
-u:For single url but without outputing the /etc/passwd.
-ut:For single url but with outputing the /etc/passwd.
-f:Read url from the url.txt and prove it if the url is vulnerable.
-c:This must be used with the parameter "-u",like:python3 CVE-2017-1000028.py -u http://xxx.xxx.xxx.xxx:4848 -c /etc/hello.txt.

Running under Python3.

I'm too bad at coding...so don't curse me when you using this shit....i'm still working on better= =!.
