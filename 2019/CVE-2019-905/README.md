# CMS-made-simple-sqli-python3
 CMS Made Simple &lt; 2.2.10 - SQL Injection (rewritten for python3),  CVE-2019-9053

 I found it problematic to run this exploit on kali linux, since python2 doesn't have termcolor, so with very few brackets I made it working with python3.
 All credit goes to: https://www.exploit-db.com/exploits/46635
 
 I tested it against a cms vulnerable machine on https://tryhackme.com .
 It is working as intended
 
 ```
 ┌──(xtafnull㉿kali)-[/opt]
└─$ python3 46635.py 
[+] Specify an url target
[+] Example usage (no cracking password): exploit.py -u http://target-uri
[+] Example usage (with cracking password): exploit.py -u http://target-uri --crack -w /path-wordlist
[+] Setup the variable TIME with an appropriate time, because this sql injection is a time based.
```
