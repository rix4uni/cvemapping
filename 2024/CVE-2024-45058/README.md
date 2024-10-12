# CVE-2024-45058
PoC for CVE-2024-45058 Broken Access Control, allowing any user with view permission in the user configuration section to become an administrator changing their own user type. 

Grab the desired nivel_usuario_ ID and run the exploit.

# Usage
```
usage: CVE-2024-45058.py [-h] -t TARGET -u USERNAME -p PASSWORD -i ID

CVE-2024-45058 exploit

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Vulnerable target
  -u USERNAME, --username USERNAME
                        Account username
  -p PASSWORD, --password PASSWORD
                        Account password
  -i ID, --id ID        nivel_usuario_ ID to be set
```
