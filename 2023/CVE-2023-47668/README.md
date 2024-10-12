# CVE-2023-47668
Restrict Content &lt;= 3.2.7 - Information Exposure via legacy log file

### Description:

The Membership Plugin – Restrict Content plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 3.2.7 via the legacy log file. This makes it possible for unauthenticated attackers to extract sensitive data including debug information.
```
Severity: medium
CVE ID: CVE-2023-47668
CVSS Score: 5.3
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
Plugin Slug: restrict-content
WPScan URL: https://www.wpscan.com/plugin/restrict-content
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/ad2d5070-ddc6-4478-abe5-776e197a4507?source=api-prod
```

POC
---

`/wp-content/uploads/rcp-debug.log`

