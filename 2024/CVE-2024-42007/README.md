# CVE-2024-42007 - php-spx Path Traversal Exploit

This repository contains a Python 3 proof-of-concept (PoC) script for CVE-2024-42007.

**Vulnerability Summary:**
> php-spx <= 0.4.15 suffers from a path traversal vulnerability via the `SPX_UI_URI` parameter, allowing unauthenticated attackers to read arbitrary files from the server.

## 🚀 Usage
python3 CVE_2024_42007.py -t http://target -f /etc/passwd
