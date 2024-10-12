# CVE-2024-33210
A cross-site scripting (XSS) vulnerability has been identified in Flatpress 1.3. This vulnerability allows an attacker to inject malicious scripts into web pages viewed by other users.

Vulnerability Type:
Cross Site Scripting (XSS)

Vendor of Product:

flatpress CMS

Affected Product Code Base:

Flatpress v1.3 - will be fixed in FlatPress version 1.3.

Affected Component:
URL

CVE Impact Other:
An attacker can exploit this vulnerability to execute arbitrary code in the context of a user's browser, potentially leading to various malicious activities such as stealing sensitive information, session hijacking, or spreading malware.

Reference:
https://medium.com/@Parag_Bagul/preventing-cross-site-scripting-xss-attacks-with-the-html-special-characters-function-in-php-1b9db17bcdb4
https://owasp.org/www-community/attacks/xss/


POC:

1.Access the following URL: http://127.0.0.1/flatpress-1.2.1/admin.php?p=entry&entry=bmnik"onmouseover="alert(1)"style="position:absolute;width:100%;height:100%;top:0;left:0;"vqtz3&action=write

2.Replace "127.0.0.1" with the domain name of the target website.

3.Inject the malicious script to trigger the XSS vulnerability.

Video POC:
https://drive.google.com/file/d/1CpVab51tsM-JXvgeSPzljhWbd91OTbxF/view

Discoverer:
Parag Bagul

