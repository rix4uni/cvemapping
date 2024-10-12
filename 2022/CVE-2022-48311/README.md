# CVE-2022-48311
HP Deskjet 2540 series printer Firmware Version CEP1FN1418BR and Product Model Number A9U23B HTTP configuration page Cross Site Scripting (XSS) Vulnerability
## Description
Cross Site Scripting (XSS) in HP Deskjet 2540 series printer Firmware Version CEP1FN1418BR and Product Model Number A9U23B allows authenticated attacker to inject their own script into the page via HTTP configuration page.
## Additional Information
Remediation uses appropriate response headers. To prevent XSS in HTTP responses that are not intended to contain any HTML or JavaScript. Using the Content-Type and X-Content-Type-Options headers ensures that browsers interpret the responses in the way intended.
## Vulnerability Type
Cross Site Scripting (XSS)
## Vendor of Product
HP
## Affected Product Code Base
HP Deskjet Ink Advantage 2540 All-in-One Printer series - Firmware Version CEP1FN1418BR and Product Model Number A9U23B
## Affected Component
HP Deskjet 2540 series printer HTTP configuration page.
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
![Alt text](https://github.com/swzhouu/CVE-2022-48311/blob/main/XSS%20Vulnerability%20in%20HP%20Deskjet%202540%20series%20printer%20HTTP%20configuration%20page.png)
