# Mezzanine-CMS-6.1.0-XSS
Mezzanine CMS 6.1.0 XSS

##### Description
###### CVE:
CVE-2025-50481
###### Affected version:
Mezzanine CMS 6.1.0
###### Base Score: 
4.8 Medium
###### Vector: 
CVSS:3.0/AV:N/AC:L/PR:H/UI:R/S:C/C:L/I:L/A:N
##### References
- https://github.com/stephenmcd/mezzanine
- https://github.com/advisories/GHSA-fpv7-hx6r-9vcx
- https://nvd.nist.gov/vuln/detail/CVE-2018-16632
##### Summary
Mezzanine CMS 6.1.0 version is affected by a stored cross-site scripting (XSS) vulnerability.

A XSS vulnerability exists in the new blog post functionality on the CMS, where an malicious authenticated attacker can craft a carefully formatted blog post containing JavaScript code, which is executed by the browser.

An attacker can leverage the XSS vulnerability to carry out attacks against the CMS website, such as defacement, or tamper with the site and cause it to be unavailable (denial-of-service).
##### Technical Description
Mezzanine CMS 6.1.0 running on Ubuntu Server 20.04.6 LTS (Focal Fossa) from pip package:
![image](https://github.com/user-attachments/assets/8aea3d50-06b2-4ff6-a5c7-32aa044a41d5)

First an authenticated attacker creates a new blog post:
![image](https://github.com/user-attachments/assets/285ac6c1-d05a-4ef4-abe8-349f12bfc17b)

Assign blog post a title:
![image](https://github.com/user-attachments/assets/6a799420-c779-42a3-9e34-f1ecccdf537d)

Create the XSS proof-of-concept (PoC) within the source code formatting of the blog post:
![image](https://github.com/user-attachments/assets/c7464fbf-b7a6-4a56-8639-92cb9fcaa828)

Save the new blog post:
![image](https://github.com/user-attachments/assets/da7301f4-4161-4289-a5e7-232b893521af)

The blog post can be published and then accessed by any user:
![image](https://github.com/user-attachments/assets/8eb05c6f-8132-4cad-9b94-ca02293abe03)

Accessing the blog post with the XSS PoC triggers the JavaScript code in the browser:
![image](https://github.com/user-attachments/assets/d8b4f919-4526-48fb-940d-ad57180fe78a)

PoC was tested using Firefox browser version 136.0 (64-bit):
![image](https://github.com/user-attachments/assets/e757d0ee-8338-46f8-adc7-6dda256278bd)

Note: Session hijacking with the XSS vulnerability is not possible, as the sessionid session cookie is not accessible, since it is configured with the HttpOnly security attribute:
![image](https://github.com/user-attachments/assets/f5dd9e61-5a21-4827-8c85-ab02addb5c52)
