# CVE-2024-25411
A cross-site scripting (XSS) vulnerability in Flatpress v1.3 allows attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the username parameter in setup.php

 Vulnerability Type : Cross Site Scripting (XSS)

Vendor of Product : https://github.com/flatpressblog/flatpress

Affected Product Code Base: Affected version : FlatPress 1.2.1 Latest - will be fixed in FlatPress version 1.3.

Affected Component:
Cross-Site Scripting (XSS) in FlatPress Installer In username parameter

Attack Type: Remote

Reference:

https://portswigger.net/web-security/cross-site-scripting

https://github.com/flatpressblog/flatpress/pull/261

Discoverer:
Parag Bagul


Step to Reproduce:

1.Download FlatPress CMS from a trusted source.

2.Start a local PHP server using the command: php -S 127.0.0.1:80

3.Open the following URL in your browser: https://127.0.0.1/setup.php

4.In the "username" field, enter the following payload: 

```html
tes"><img src=x onload=alert(1)>

'''

5.Click on the "Next" button.

6.A pop-up with the number "1" will appear on the screen, indicating the successful execution of the payload.
