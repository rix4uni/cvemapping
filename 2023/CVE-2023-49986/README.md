# CVE-2023-49986
# School Fees Management System v1.0 - Cross-Site Scripting (XSS) Vulnerability in "name" parameter on "add_new_parent"

**Description**: A cross-site scripting (XSS) vulnerability in the component “add_new_parent” of School Fees Management System 1.0 allow attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the “name” parameter. 

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49986  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit the vulnerability, a user with appropriate permissions must access the "/ci_fms/admin/parent" page. On this page, the user should add a new parent. The malicious payload needs to be inserted into the  'name' or 'email' parameters.
**Payload:**: 
```
<script>alert(document.domain)</script>
```

Discoverer(s)/Credits:  
Geraldo Alcântara
