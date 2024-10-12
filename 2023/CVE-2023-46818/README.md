# CVE-2023-46818 exploit

This is a python version of the original php script for the vulnerability affecting ispconfig 3.2.11 and previous versions.

Original PHP source: https://packetstormsecurity.com/files/176126/ISPConfig-3.2.11-PHP-Code-Injection.html

This proof-of-concept is intended for educational purposes only.

## Usage

```
python exploit.py http://10.10.10.10/ adminuser passwd
```
## Vulnerability description

User input passed through the "records" POST parameter to
/admin/language_edit.php is not properly sanitized before being used
to dynamically generate PHP code that will be executed by the
application. This can be exploited by malicious administrator users to
inject and execute arbitrary PHP code on the web server.

## Credits

Credits to Egidio Romano.
