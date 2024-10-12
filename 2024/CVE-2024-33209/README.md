# CVE-2024-33209
FlatPress 1.3. is vulnerable to Cross Site Scripting (XSS). An attacker can inject malicious JavaScript code into the "Add New Entry" section, which allows them to execute arbitrary code in the context of a victim's web browser.

Vulnerability Type:
Cross Site Scripting (XSS)

Vendor of Product :

flatpress CMS

Affected Product Code Base : 

Flatpress v1.3 - will be fixed in FlatPress version 1.3.

Affected Component

Add New Entry feature in admin panel

Attack Type:

Remote

Impact:
An attacker exploiting this vulnerability could inject malicious code into the FlatPress CMS, which could lead to various malicious activities such as stealing user session tokens, cookies, or other sensitive information. They can also modify the content of the webpage, redirect users to malicious websites, or perform actions on behalf of the victim.

Attack Vectors:

Attacker can send crafted link to victim.

Reference

https://owasp.org/www-community/attacks/xss/

Video POC:

https://drive.google.com/file/d/1AvPQszOimG8_zxiwoVnmeGGh8JY9J4IL/view

Discoverer:

Parag Bagul
