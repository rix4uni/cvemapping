# CVE-2022-3949
XSS in Simple Cashiering System


Simple Cashiering System is vulnerable to Cross Site Scripting (XSS) - a malicious actor can change the fullname of a compromised user to a XSS Payload and whenever a admin visits the user-tab or the sales tab (and looks into sales made by the malicious actor) the payload is triggered. This can lead to session takeover because the cookie does not have an HttpOnly Flag. 

How-to Reproduce:
* Download https://www.sourcecodester.com/php/14945/simple-cashiering-system-pos-php-and-sqlite-source-code-free-download.html
* setup web server with php + sqlite3 and copy the application to the webserver
* login as user and change your fullname to <script>javascript:alert(document.cookie)</script>
* login as an admin user and visit the user tab of the admin dashboard
* XSS is triggered
<img width="797" alt="step1" src="https://user-images.githubusercontent.com/20245897/201341015-7bec2a98-40d7-4188-8d5c-404a24d10255.png">
<img width="723" alt="step2" src="https://user-images.githubusercontent.com/20245897/201341056-8a6134c8-861b-4fe5-b8f7-4a3f98da4000.png">
