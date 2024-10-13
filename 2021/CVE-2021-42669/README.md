# CVE-2021-42669
CVE-2021-42669 - Remote code execution via unrestricted file upload vulnerability in the Engineers online portal system.

# Technical description:
A unrestricted file upload vulnerability exists in the Engineers Online Portal system. An attacker can leverage this vulnerability in order to get a remote code execution on the affected web server. 
Once an avatar gets uploaded it is getting uploaded to the /admin/uploads/ directory, and is accessible by all users. 
By uploading a simple php webshell the attacker can gain remote code execution on the web server. 

Affected components - 

Vulnerable page - teacher_avatar.php

# CVE-2021-42669.py usage - 
```
# Upload a simple webshell to the target machine - 
python CVE-2021-42669.py <target_ip> <target_port> <target_uri> <username> <password>
```

## Example -
```
python CVE-2021-42669.py 127.0.0.1 80 /nia_uoz_monitoring_system/ MyUserName MyPassword
```

# Proof of concept (Poc) - 

![CVE-2021-42669](https://user-images.githubusercontent.com/93016131/140194579-79107b2f-b511-435f-874c-961b4636df9c.gif)

# Refernces - 
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42669

https://nvd.nist.gov/vuln/detail/CVE-2021-42669

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 
