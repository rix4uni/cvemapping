# CVE-2024-25412
A cross-site scripting (XSS) vulnerability in Flatpress v1.3 allows attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the email field

Vulnerability Type:

Cross Site Scripting (XSS)

Vendor of Product:

https://github.com/flatpressblog/flatpress

Affected Product Code Base

Affected version :FlatPress 1.2.1 Latest - will be fixed in FlatPress version 1.3.

Affected Component:

Cross-Site Scripting (XSS) in FlatPress Installer (email parameter)

Attack Type:

Remote

Discoverer:

Parag Bagul

Reference:

https://portswigger.net/web-security/cross-site-scripting

https://drive.google.com/file/d/1GBL-iY5ZRaxRqLVqpBe1w6dVgEfywAG7/view?usp=sharing

Step to Reproduce:

1.Download the FlatPress CMS from a trustworthy source. (https://github.com/flatpressblog/flatpress)

2.Launch a local PHP server using the command: php -S 127.0.0.1:80

3.Open the following URL in your browser: https://127.0.0.1/setup.php

4. Within the **"email"** field, insert the subsequent payload. A pop-up displaying the number **"1"** will appear on the screen, confirming the successful execution of the payload. After that, proceed by clicking the **"Next"** button.

```html

"><img src=x onload=alert(1)> or "><script>alert(1)</script>
'''





