# CVE-2023-49976
# Customer Support System 1.0 - (XSS) Cross-Site Scripting Vulnerability in the "subject" at "ticket_list"

**Description**: Customer Support System 1.0 is vulnerable to stored XSS. A XSS vulnerability exists in version 1 of the Customer Support System. A malicious actor can insert JavaScript code through the "subject" field when editing/creating a ticket. The code is executed whenever the page "/customer_support/index.php?page=ticket_list" is visited.  

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49976  
**Tested on**: Windows  
### Steps to reproduce:  
1. Log in to the application.  
2. Visit the ticket creation/editing page.
3. Create/Edit a ticket and insert the malicious payload into the "subject" field/parameter.
4. Payload:
```
<dt/><b/><script>alert(document.domain)</script>
```     

Saving the ticket and injecting the payload.  

![xss01](https://github.com/geraldoalcantara/xss-ticket-Customer_Support_System/assets/152064551/0ed1719d-4683-4a49-9e36-c7afd9b3c6f1)   

Visiting the ticket listings page, successful execution of the attack.  
<div align="center">
  <img src="https://github.com/geraldoalcantara/xss-ticket-Customer_Support_System/assets/152064551/ef710f8a-f03d-4ae8-bd89-f02309940141" alt="xss03">
  <img src="https://github.com/geraldoalcantara/xss-ticket-Customer_Support_System/assets/152064551/67533fdd-14fc-4440-9187-37d002e13821" alt="xss03">
</div>

Discoverer(s)/Credits:  
Geraldo Alcântara  
