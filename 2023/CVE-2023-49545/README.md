# CVE-2023-49545
# Customer Support System 1.0 - Directory Listing

**Description**:  A directory listing vulnerability in Customer Support System v1 allows attackers to list directories and sensitive files within the application without requiring authentication/authorization.

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49545  
**Tested on**: Windows  
### Steps to reproduce:   

1. Navigate to URL: http://{IP}/customer_support/database/ or http://{IP}/customer_support/assets/. I found out that many important files of application can be accessed directly from this directory listing.  

Accessing the directory /database/  

![db](https://github.com/geraldoalcantara/dir-list-Customer_Support_System/assets/152064551/a1219b75-8aa9-4e4a-bbba-8b2434163833)

Accessing the directory /assets/  

![asset](https://github.com/geraldoalcantara/dir-list-Customer_Support_System/assets/152064551/f9c5705c-a0b8-47aa-9ee5-98fba238f4a6)


Discoverer(s)/Credits:  
Geraldo Alcântara  
