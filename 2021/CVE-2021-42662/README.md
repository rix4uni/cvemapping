# CVE-2021-42662
CVE-2021-42662 - Stored Cross-Site Scripting vulnerability in the Online event booking and reservation system version 2.3.0. 

# Technical description:
A stored XSS vulnerability exists in the Event management software version 2.3.0. An attacker can leverage this vulnerability in order to run javascript on the web server surfers behalf, which can lead to cookie stealing, defacement and more. 

Affected components - 

Vulnerable page - HOLY

Vulnerable parameter - "reason"

# Steps to exploit:
1) Navigate to http://localhost/event-management/views/?v=HOLY
2) Insert your payload in the "reason" parameter
3) Click "Add holiday"

# Proof of concept (Poc) -
The following payload will allow you to run the javascript code - 
```
<script>alert("This is an XSS")</alert>
```

![CVE-2021-42662](https://user-images.githubusercontent.com/93016131/140184846-6b92b6c9-74fd-4ba0-816b-75e9218db2e3.gif)

# References - 
https://www.exploit-db.com/exploits/50450

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42662

https://nvd.nist.gov/vuln/detail/CVE-2021-42662


# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 

