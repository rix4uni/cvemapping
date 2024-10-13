# CVE-2021-42663
CVE-2021-42662 - HTML Injection vulnerability in the Online event booking and reservation system version 2.3.0. 

# Technical description:
A HTML injection vulnerability exists in the Online Event Booking and Reservation System version 2.3.0. An attacker can leverage this vulnerability in order to change the visibility of the website. Once the target user clicks on a given link he will display the content of the HTML code of the attacker's choice.

Affected components - 

Vulnerable page - index.php

Vulnerable parameter - "msg"

# Steps to exploit:
1) Navigate to http://localhost/event-management/views/index.php
2) Insert your payload in the "msg" parameter through the URL
3) Send the complete link to the victim


# Proof of concept (Poc) -
The following payload will allow you to run the HTML code - 
```
<h1>This is an HTML injection</h1>
```

![CVE-2021-42663](https://user-images.githubusercontent.com/93016131/140179296-b2fbb220-94a7-4f97-aae9-7ad63755f95b.gif)

# References - 
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42663

https://nvd.nist.gov/vuln/detail/CVE-2021-42663

# Discovered by -
Alon Leviev(0xDeku), 22 October, 2021. 
