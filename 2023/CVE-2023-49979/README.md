# CVE-2023-49979
# Best Student Management System v1.0 - Incorrect Access Control - Directory Listing

**Description**:  A directory listing vulnerability in Best Student Management System v1.0 allows attackers to list directories and sensitive files within the application without requiring authentication/authorization.

**Vulnerable Product Version**: Best Student Management System v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49979  
**Tested on**: Windows  
### Steps to reproduce:   

1. Navigate to URL: http://{IP}/upresult/includes/ or http://{IP}/upresult/assets/. I found out that many important files of application can be accessed directly from this directory listing.  

Discoverer(s)/Credits:  
Geraldo Alcântara  
