# CVE-2025-49071
Flozen < 1.5.1 - Unauthenticated Arbitrary File Upload

### Description :

Flozen Theme < 1.5.1 - Unauthenticated Arbitrary File Upload
Description
The Flozen Theme for WordPress (versions up to and including 1.5.1) is vulnerable to unauthenticated arbitrary file upload, due to missing authentication checks and insufficient file type validation in the flozen_add_new_custom_font() function. This allows unauthenticated attackers to upload arbitrary ZIP files containing malicious PHP code (e.g., webshell), which are automatically extracted to `wp-content/uploads/nasa-custom-fonts/`, leading to full remote code execution (RCE).


# INFO : [**CVE-2025-49071**](https://www.wordfence.com/threat-intel/vulnerabilities/wordpress-themes/flozen-theme/flozen-151-unauthenticated-arbitrary-file-upload)

~ **CVSS Score: 9.8 (Critical)** 

~ **Affected Versions: < 1.5.1**

- Researcher : [**Phat RiO - BlueRock**](https://www.wordfence.com/threat-intel/vulnerabilities/researchers/phat-nguyen)

### usage :

- make sure shadow.zip is in the directory
- python/python3 shadow.py
- input target file name
- input thread 5-50 max

### features :

- Multi-threading
- Error Handling
- Scanner + Exploit
- Verification Shell
- Auto-Save Results

### output :
  
```bash

- [?] Enter filename with targets: list.txt
- [?] Enter threads (5-50): 50
- [*] Loading targets...
- [+] Loaded 267 targets
- [*] Starting 50 threads...
- [!] Gak Ada Bro Themes nya!: http://target.com
- [+] Gas Exploit Cuk! http://example.com/ | Version: 1.2.8 🚩💉
- [+] Shell Ada Bro! http://example.com/wp-content/uploads/nasa-custom-fonts/shadow/index.php

```
## Disclaimer :

## This tool is for educational and security testing purposes only.
Unauthorized use of systems you don't own or don't have permission to test is illegal.
