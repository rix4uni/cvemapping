# CVE-2023-46948 - Reflected XSS in Temenos T24 R19.40

A reflected Cross-Site Scripting (XSS) vulnerability was found on Temenos T24 Browser R19.40 that enables a remote attacker to execute arbitrary JavaScript code in an authenticated victim browser-based web console.

Affected Product: Temenos T24 - R19.40 

Affected Components:
- /BrowserWebR19/jsps/about.jsp
- /BrowserWebR19/jsps/genrequest.jsp

Affected parameter: 'skin'

Request:
![image](https://github.com/user-attachments/assets/c9b08ae5-040a-4f00-99b0-d3a3e78628c4)


Response:
![image](https://github.com/user-attachments/assets/c711d086-68b9-4b17-b1cb-d6a5d22477c7)


Remediation:


Timeline:
- Discovered | 4/10/2023
- Reported to vendor | 19/10/2023
- Requested CVE ID |25/10/2023
- CVE validated | 06/11/2023
