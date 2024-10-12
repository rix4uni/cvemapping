# CVE-2023-46015-Code-Projects-Blood-Bank-1.0-Reflected-Cross-Site-Scripting-Vulnerability
+ Exploit Author: ersinerenler
# Vendor Homepage
+ https://code-projects.org/blood-bank-in-php-with-source-code
# Software Link
+ https://download-media.code-projects.org/2020/11/Blood_Bank_In_PHP_With_Source_code.zip
# Overview
+ Code-Projects Blood Bank V1.0 is susceptible to a significant security vulnerability involving Reflected Cross-Site Scripting (XSS) through the 'msg' parameter in the index.php file. The application fails to adequately sanitize user-supplied data, making it prone to script injection attacks. An attacker can exploit this issue to execute arbitrary script code in the browser of unsuspecting users, potentially compromising their security and privacy within the affected site.
# Vulnerability Details
+ CVE ID: CVE-2023-46015
+ Affected Version: Blood Bank V1.0
+ Vulnerable File: /index.php
+ Parameter Name: msg
+ Attack Type: local
# References:
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46015
+ https://nvd.nist.gov/vuln/detail/CVE-2023-46015
# Description
+ The 'msg' parameter in the index.php file of Code-Projects Blood Bank V1.0 is susceptible to Reflected Cross-Site Scripting (XSS). This vulnerability arises due to insufficient input validation and sanitation of user-supplied data. An attacker can exploit this weakness by injecting malicious scripts into the 'msg' parameter, which, when executed, could compromise the user's browser within the context of the affected site.
# Proof of Concept (PoC) : 
+ Payload: `<div><svg/onload=alert(document.domain)>`
+ `http://localhost/bloodbank/index.php?msg=<div><svg/onload=alert(document.domain)>`
<img width="1447" alt="image" src="https://github.com/ersinerenler/CVE-2023-46015-Code-Projects-Blood-Bank-1.0-Cross-Site-Scripting-Vulnerability/assets/113091631/d16f3a62-fb4c-421a-a8a0-7c13fce75d01">

