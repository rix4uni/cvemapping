# CVE-2023-40600
EWWW Image Optimizer &lt;= 7.2.0 - Unauthenticated Sensitive Information Exposure via Debug Log

### Description

The EWWW Image Optimizer plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 7.2.0 via the debug_log function. This makes it possible for unauthenticated attackers to extract sensitive debug data when debug logging is enabled.

```
Severity: medium
CVE ID: CVE-2023-40600
CVSS Score: 5.3
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
Plugin Slug: ewww-image-optimizer
WPScan URL: https://www.wpscan.com/plugin/ewww-image-optimizer
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/d20ff1a8-8794-41e1-9e66-1cda90f9ff77?source=api-prod
Diff URL: https://plugins.trac.wordpress.org/changeset?sfp_email=&sfph_mail=&reponame=&new=2964259%40ewww-image-optimizer&old=2941029%40ewww-image-optimizer&sfp_email=&sfph_mail=
```

POC
---

```
 /wp-content/plugins/ewww-image-optimizer/debug.log
```
