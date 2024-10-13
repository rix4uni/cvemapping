# CVE-2020-10128 - SearchBlox product before V-9.2.1 is vulnerable to Stored-Cross Site Scripting

**Product Description:** SearchBlox simplifies enterprise search for complex organizations. SearchBlox intuitive and intelligent tools offer out-of-the-box setup, secure encryption, and low total cost of ownership. AI-powered solutions optimize each step of the search journey to dramatically improve engagement. SearchBlox is the easy choice for leaders in financial services, healthcare, and government.

**Description:** SearchBlox before Version 9.2.1 is vulnerable to Stored Cross Site Scripting.

**Vulnerability Type:** Stored Cross Site Scripting

**Severity Rating:** High

**Vendor of Product:** SearchBlox

**Affected Product Code Base:** SearchBlox-9.2

**Affected Component:** SearchBlox product with version before 9.2.1 is vulnerable to stored cross-site scripting at multiple user input parameters. In SearchBlox products multiple parameters are not sanitized/validate properly which allows an attacker to inject malicious JavaScript.

**Attack Type:** Remote

**Impact Information Disclosure:** True

**Attack Vectors:** To exploit this vulnerability attacker must enter XSS payload at multiple vulnerable parameters.
                      http://<Web-Interface-URLs>/searchblox/admin/main.jsp?menu1=adm 
                      
**Has the vendor confirmed or acknowledged the vulnerability?:** True

**Reference:** [Version 9.1 (searchblox.com) ](https://developer.searchblox.com/v9.2/changelog/version-91) & [Version 9.2.1 (searchblox.com) ](https://developer.searchblox.com/v9.2/changelog/version-921)

**Exploit Author:** Amar Kaldate

**Contact:** [ Amar Kaldate | LinkedIn ](https://www.linkedin.com/in/amar-kaldate/)
