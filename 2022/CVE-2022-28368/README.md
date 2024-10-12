# CVE-2022-28368 - Dompdf RCE
Dompdf RCE PoC Exploit

![alt text](https://rvizx.github.io/cve-2022-28368/img.png?raw=true)

<p align="center"> <a href="https://www.exploit-db.com/exploits/51270"> <img src="https://rvizx.github.io/assets/exploitdb.png" alt="ExploitDB"> </a> </p>

Dompdf versions <1.2.1 are vulnerable to Remote Code Execution (RCE) by injecting CSS into the data. The file can be tricked into storing a malicious font with a .php file extension in its font cache, which can later be executed by accessing it from the web.

# Usage
```
git clone https://github.com/rvizx/CVE-2022-28368
cd  CVE-2022-28368
python3 -m pip install -r requirements.txt
python3 dompdf-rce.py --help
```

# Credits & Notes
Positive Security - https://positive.security/blog/dompdf-rce
