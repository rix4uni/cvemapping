# CVE-2024-0757 (Exploit)
## Description
The Insert or Embed Articulate Content into WordPress plugin for WordPress is vulnerable to arbitrary file uploads through insecure file uploads in a zip archive in all versions up to, and including, 4.3000000023. This makes it possible for unauthenticated attackers to upload zip files containing phar files on the affected site's server which may make remote code execution possible.

> [!IMPORTANT]
> CVSS:	**8.8 (High)** [CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H]  
> Software Type:	**Plugin**  
> Software Slug:	**insert-or-embed-articulate-content-into-wordpress**  
> Affected Version:	**<= 4.3000000023**  

## Exploit
1. Clone the exploit
``` bash
  git clone https://github.com/hunThubSpace/CVE-2024-0757-Exploit.git && cd CVE-2024-0757-Exploit
```
2. Install requirements
``` bash
  pip install -r requirements.txt
```
3. Run exploit
``` bash
  python3 exploit.py
```
4. Browse to given url and click on **Go to shell page**
5. You have a shell :)

## PoC video
https://github.com/hunThubSpace/CVE-2024-0757-Exploit/assets/49031710/6855e8c4-a00b-469d-bcec-7b2252352ee4

