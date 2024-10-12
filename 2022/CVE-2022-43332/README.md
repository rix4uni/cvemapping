# CVE-2022-43332
Cross Site Scripting in WonderCMS

Description:
A cross-site scripting (XSS) vulnerability in Wondercms v3.3.4 allows potential attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the Site title field of the Configuration Panel - coupled with the fact that the cookie has no HttpOnly Flag this could be used to steal cookies of logged-in users. 

How to Reproduce:
To reproduce one can download the zip file provided at wondercms.com (3.3.4), unzip it to a web server and after login with the password provided on the homepage in the settings menu the title can be adjusted - the vulnerability can be triggered with the following payload: <script>javascript:alert(document.cookie)</script>
