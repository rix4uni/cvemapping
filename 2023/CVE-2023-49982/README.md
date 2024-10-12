# CVE-2023-49982
# School Fees Management System v1.0 - Incorrect Access Control - Privilege Escalation

**Description**: Broken access control in School Fees Management System v1.0 allows attackers to escalate privileges and perform Administrative actions, including adding and deleting user accounts.

**Vulnerable Product Version**: School Fees Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 29/11/2023  
**Confirmed on**: 15/12/2023  
**CVE**: CVE-2023-49982  
**Tested on**: Windows  
**Affected Components**:
> /ci_fms/admin/management/class  
> /ci_fms/admin/management/term  
> /ci_fms/admin/management/users  
> /ci_fms/admin/management/settings  
### Steps to reproduce:  
Unauthorized access to any page of the application and performing unrestricted actions is possible. To exploit the vulnerability, an attacker must log in as a user and directly access administrative URLs like http://{IP}/ci_fms/admin/management/users, executing desired actions.

Discoverer(s)/Credits:  
Geraldo Alcântara  
