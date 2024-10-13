# CVE-2020-26732
SKYWORTH GN542VF Hardware Version 2.0 and Software Version 2.0.0.16 does not set the Secure flag for the session cookie in an HTTPS session
## Description
SKYWORTH GN542VF Hardware Version 2.0 and Software Version 2.0.0.16 does not set the Secure flag for the session cookie in an HTTPS session, which makes it easier for remote attackers to capture this cookie by intercepting its transmission within an HTTP session.
## Additional Information
Each cookie should be carefully reviewed to determine if it contains sensitive data or is relied upon for a security decision. If possible, ensure all communication occurs over an encrypted channel and add the secure attribute to all session cookies or any cookies containing sensitive data.
## VulnerabilityType Other
Web Application Cookies Not Marked Secure
## Vendor of Product
SKYWORTH
## Affected Product Code Base
SKYWORTH GN542VF - Hardware Version 2.0 and Software Version 2.0.0.16
## Affected Component
Web Application Cookies of SKYWORTH GN542VF.
## Attack Type
Local
## Impact Information Disclosure
true
## Attack Vectors
This means the cookie could potentially be stolen by an attacker who can successfully intercept and decrypt the traffic, or following a successful man-in-the-middle attack.
## Discoverer
Jiraput Thamsongkrah
## Proof of Concept
![Alt text](https://github.com/swzhouu/CVE-2020-26732/blob/main/SKYWORTH%20GN542VF%20Hardware%20Version%202.0%20and%20Software%20Version%202.0.0.16%20does%20not%20set%20the%20Secure%20flag%20for%20the%20session%20cookie%20in%20an%20HTTPS%20session.png)
