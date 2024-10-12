# CVE-2023-49543
# Book Store Management System v1.0 - Incorrect Access Control 


**Description**: Incorrect access control in Book Store Management System v1 allows attackers to access unauthorized pages and execute administrative functions without authenticating.

**Vulnerable Product Version**: Book Store Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 29/11/2023  
**Confirmed on**: 15/12/2023  
**CVE**: CVE-2023-49543  
**Tested on**: Windows  
**Impact**: Unauthorized users can modify passwords and user attributes, leading to account takeover.  
### Steps to reproduce:  
Unauthorized access to any page of the application and performing unrestricted actions is possible. You can simply access the "/bsms_ci/index.php/user" page and create, edit, or delete users, for example.

Discoverer(s)/Credits:  
Geraldo Alcântara  
