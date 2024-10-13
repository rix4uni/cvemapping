# CVE-2021-42665
CVE-2021-42665 - SQL Injection authentication bypass vulnerability in the Engineers online portal system. 
 
# Technical description:
An SQL Injection vulnerability exists in the Engineers Online Portal login form which can allow an attacker to bypass authentication. 

Affected components - 

Vulnerable page - login.php

Vulnerable parameter - "username", "password"

# Steps to exploit:
1) Navigate to http://localhost/nia_munoz_monitoring_system/login.php
2) Insert your payload in the username or password field 
3) Click login

# Proof of concept (Poc) -
The following payload will allow you to bypass the authentication mechanism of the Engineers Online Portal login form - 
```
sqli' OR '1'='1';-- -
```

![CVE-2021-42665](https://user-images.githubusercontent.com/93016131/140184038-d7e03847-ccf5-434e-bf5d-27ce4da2665e.gif)

# References - 
https://www.exploit-db.com/exploits/50452

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42665

https://nvd.nist.gov/vuln/detail/CVE-2021-42665

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 

