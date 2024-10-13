# CVE-2021-42664
CVE-2021-42664 - Stored Cross-Site Scripting vulnerability in the Engineers online portal system. 

# Technical description:
A stored XSS vulnerability exists in the Engineers online portal system. An attacker can leverage this vulnerability in order to run javascript on the web server surfers behalf, which can lead to cookie stealing, defacement and more. 

Affected components -  

Vulnerable page - add_quiz.php

Vulnerable parameters - "quiz_title", "description"

# Steps to exploit:
1) Navigate to http://localhost/nia_munoz_monitoring_system/add_quiz.php
2) Insert your payload in the "quiz_title" parameter or the "description" parameter
3) Click save

# Proof of concept (Poc) -
The following payload will allow you to run the javascript code - 
```
<script>alert("This is an XSS")</script>
```

![CVE-2021-42664](https://user-images.githubusercontent.com/93016131/140181371-4ebb424b-a550-40c7-843a-9cbeacd9bb34.gif)

# References -
https://www.exploit-db.com/exploits/50451

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42664

https://nvd.nist.gov/vuln/detail/CVE-2021-42664

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 
