# CVE-2023-49981
# School Fees Management System v1.0 - Incorrect Access Control - Directory Listing

**Description**: A directory listing vulnerability in School Fees Management System v1.0 allows attackers to list directories and sensitive files within the application without requiring authentication/authorization.

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49981  
**Tested on**: Windows  
### Steps to reproduce:   
### Affected Components:  
> /ci_fms/database/  
> /ci_fms/uploads/  
> /ci_fms/assets/  
> /ci_fms/assets/backend/  

1.  To exploit the vulnerability, an attacker simply needs to navigate to the directories. Navigate to URL: http://{IP}/ci_fms/database/,  http://{IP}/ci_fms/uploads/ or http://{IP}/ci_fms/assets/. I found out that many important files of application can be accessed directly from this directory listing.  

Discoverer(s)/Credits:  
Geraldo Alcântara  
