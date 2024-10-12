# CVE-2023-49977
# Customer Support System 1.0 - Cross-Site Scripting (XSS) Vulnerability in "Address" field/parameter on "customer_list" Page

**Description**: Customer Support System 1.0 is vulnerable to stored XSS. A XSS vulnerability exists in version 1 of the Customer Support System. A malicious actor can insert JavaScript code through the "Address" field/parameter when editing/creating a customer. The code is executed whenever the page "/customer_support/index.php?page=customer_list" is visited.  

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49977  
**Tested on**: Windows  
### Steps to reproduce:  
1. Log in to the application.  
2. Navigate to "/customer_support/index.php?page=customer_list" to edit an existing customer or "/customer_support/index.php?page=new_customer" to create a new customer.
3. Create or edit a customer and insert the malicious payload into the "Address" field/parameter.  
4. Payload:
```
</dt></b><script>alert(document.domain)</script>
```     

Discoverer(s)/Credits:  
Geraldo Alcântara
