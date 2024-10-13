# CVE-2020-26733
SKYWORTH GN542VF Hardware Version 2.0 and Software Version 2.0.0.16 Cross Site Scripting (XSS) Vulnerability
## Description
Cross Site Scripting (XSS) in Configuration page in SKYWORTH GN542VF Hardware Version 2.0 and Software Version 2.0.0.16 allows authenticated attacker to inject their own script into the page via DDNS Configuration Section.
## Additional Information
Remediation uses appropriate response headers. To prevent XSS in HTTP responses that are not intended to contain any HTML or JavaScript. Using the Content-Type and X-Content-Type-Options headers ensures that browsers interpret the responses in the way intended.
## Vulnerability Type
Cross Site Scripting (XSS)
## Vendor of Product
SKYWORTH
## Affected Product Code Base
SKYWORTH GN542VF - Hardware Version 2.0 and Software Version 2.0.0.16
## Affected Component
DDNS Configuration Section in Configuration page of SKYWORTH GN542VF Router.
## Attack Type
Local
## Impact Code execution
true
## Impact Information Disclosure
true
## CVE Impact Other
Disclosure of the user's session cookie, allowing an attacker to hijack the user's session and take over the account.
## Attack Vectors
To exploit the vulnerability, the attacker must be authenticated.
## Discoverer
Jiraput Thamsongkrah
## Proof of Concept
![Alt text](https://github.com/swzhouu/CVE-2020-26733/blob/main/SKYWORTH%20GN542VF%20Hardware%20Version%202.0%20and%20Software%20Version%202.0.0.16%20Cross%20Site%20Scripting%20(XSS)%20Vulnerability.png)
