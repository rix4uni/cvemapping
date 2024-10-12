# CVE-2023-49978
# Customer Support System 1.0  - Incorrect Access Control 


**Description**: Incorrect access control in Customer Support System v1 allows non-administrator users to access administrative pages and execute actions reserved for administrators.

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 29/11/2023  
**Confirmed on**: 15/12/2023  
**CVE**: CVE-2023-49978  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit this vulnerability, an attacker needs a low-privilege user. Afterward, they simply have to directly access URLs with administrative functions through a web browser.
It is possible for the user to modify attributes of other users, including passwords, delete users, and so on.

Examples of Administrative Pages Accessible to Non-Administrator Users and Actions They Can Perform:

* /customer_support/index.php?page=staff_list -> Edit/Delete Staff Users
* /customer_support/index.php?page=new_staff -> Add New Staff User
* /customer_support/index.php?page=customer_list -> Edit/Delete Customer Users

Discoverer(s)/Credits:  
Geraldo Alcântara  
