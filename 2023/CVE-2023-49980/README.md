# CVE-2023-49980
# Best Student Result Management System 1.0 - Directory Listing

**Description**: Best Student Result Management System 1.0 is vulnerable to Broken Access Control. The Directory Listing vulnerability allows any remote attacker to view the application's sensitive files within the includes and assets directories of the application without any authorization.

**Vulnerable Product Version**: Best Student Result Management System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49980   
**Tested on**: Windows  
### Steps to reproduce:  
1. Navigate to URL: http://{IP}/upresult/includes/ or http://{IP}/upresult/assets/. I found out that many important files of application can be accessed directly from this directory listing.  

Accessing the directory /includes/  
![dir01](https://github.com/geraldoalcantara/dir-listin-Best_Student_Result_Management_System/assets/152064551/3f06fea7-0265-482c-9d1c-0c14575d2e33)  

Accessing the directory /assets/  
![dir02](https://github.com/geraldoalcantara/dir-listin-Best_Student_Result_Management_System/assets/152064551/e06b7357-b22a-4a60-a55c-c92b5c67ed01)  

Discoverer(s)/Credits:  
Geraldo Alcântara
