# CVE-2023-49987
# School Fees Management System v1.0 - Cross-Site Scripting (XSS) Vulnerability in "tname" parameter on "new_term"

**Description**: A cross-site scripting (XSS) vulnerability in the component “new_term” of School Fees Management System 1.0 allow attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the “tname” parameter. 

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49987  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit the vulnerability, a user with appropriate permissions must access the "/ci_fms/admin/management/term" page. On this page, the user should either edit an existing term or add a new one. The malicious payload needs to be inserted into the "tname" parameter during this process.
**Payload:**: 
```
<script>alert(document.domain)</script>
```

Discoverer(s)/Credits:  
Geraldo Alcântara
