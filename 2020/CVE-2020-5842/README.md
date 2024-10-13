# [CVE-2020-5842 Stored XSS Vulnerability in Codoforum 4.8.3](https://prasanthk.com/index.php/2020/01/16/cve-2020-5842-stored-xss-vulnerability-in-codoforum-4-8-3/)

Listed in: [Exploit-db](https://www.exploit-db.com/exploits/47876), [Cve Mitre](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-5842) and [The daily swig](https://portswigger.net/daily-swig/codoforum-software-patched-against-stored-xss-vulnerability)

While I was searching for a free forum software for our community I found Codoforum. After installing it We (Vyshnav Vizz) tried a few simple XSS payloads to ensure the security and suddenly got surprised with finding of multiple critical cross site scripting vulnerability which affects admin users. Thanks a lot my brother (Vyshnav Vizz) for supporting me throughout my life.

Affected component : User Registration page

Attack vector
This vulnerability can results attacker to inject the XSS payload in User Registration section and each time admin visits the manage user section from admin panel, the XSS triggers and attacker can able to steal the cookie according to the crafted payload.

Additional information
A Critical (Stored XSS) Cross Site Scripting Vulnerability found in Codoforum v4.8.3 which is the latest version last updated on Oct 29th 2019.

Codoforum User registration mechanism is critically vulnerable to Stored Cross site scripting issue. A user can be created from register page using a crafted XSS payload in the user field. As a result a user will be created with XSS payload.
If the admin visits the user manage section using admin dashboard section from manage user section XSS got triggers. Due to this Stored XSS vulnerability which stores in the server, each time admins visit the page the XSS payload got triggers.

Recreation Steps
1. Download and Install Codoforum 4.8.3 in a local server.
https://codoforum.com/buy
![image](https://user-images.githubusercontent.com/58906808/153190114-b9749d74-87fd-4528-be5f-37b98f389277.png)


2. Browse http://localhost/index.php?u=/user/register and create a user with payload below.

Username : “><svg/onload=alert(1)>
Password : password
Email : c41m@email.com
Injecting payload
![image](https://user-images.githubusercontent.com/58906808/153190180-f2de6db3-2ed5-4e08-a79a-5bafc6aee135.png)


3. Now browse http://localhost/admin/index.php?page=users/manage, a XSS will be triggered here.
Stored XSS got triggered
![image](https://user-images.githubusercontent.com/58906808/153190268-0c06f4bb-d2fa-4e8e-9b7a-f01ccbef2382.png)


Mitigation

Input validation and output sanitization and escaping will make application safe.

Timeline

Discovered: Jan 3 2020
Reported to Codologic: Jan 3 2020
Acknowledged by Codologic: Jan 3 2020
Listed in exploit-db.com: Jan 6 2020
Listed in cve.mitre.org: Jan 6 2020
