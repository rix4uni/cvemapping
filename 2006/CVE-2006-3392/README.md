# CVE-2006-3392

About the vulnerability
-----------------------
A vulnerability has been reported in Webmin and Usermin, which can be exploited by malicious people to disclose potentially sensitive information. The vulnerability is caused due to an unspecified error within the handling of an URL. This can be exploited to read the contents of any files on the server via a specially crafted URL, without requiring a valid login. The vulnerability has been reported in Webmin (versions prior to 1.290) and Usermin (versions prior to 1.220). 

This small script helps to avoid using MetaSploit (msfconsole) during the Enterprise pentests and OSCP-like exams.
Grep included function will help you to get only the important information.

Usage example:
--------------
```
nano CVE-2006-3392.sh
change an IP-address (ctrl+O, ctrl+X)
chmod +x CVE-2006-3392.sh
./CVE-2006-3392.sh /etc/passwd
```
or
```
./CVE-2006-3392.sh /etc/passwd bash
```


An original article:
--------------------
[https://www.ivanglinkin.com/CVE-2006-3392/](https://www.ivanglinkin.com/CVE-2006-3392/)


Video example:
--------------
![](https://github.com/IvanGlinkin/media_support/blob/main/CVE-2006-3392-Video.gif?raw=true)


Screenshots:
------------
![](https://github.com/IvanGlinkin/media_support/blob/main/CVE-2006-3392-image.gif?raw=true)

