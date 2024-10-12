# Snipe-IT Version v6.0.2

### Vulnerability Explanation:
An arbitrary file upload vulnerability in the Update Branding Settings component of Snipe-IT v6.0.2 allows attackers to execute arbitrary code via a crafted file.

### Attack Vectors:
- We found a vulnerability file upload, when we upload malicious file at Update Branding Settings page.

### Payload :
https://github.com/bypazs/GrimTheRipper/blob/main/GrimTheRipperTeam.svg

### Tested on:
1.  Snipe-IT Version v6.0.2
2.  Google Chrome Version 102.0.5005.61 (Official Build) (64-bit)

### Affected Component: 
- Affected in Branding Settings page on favicon tab (http://<IP>/uploads/malicious_file.svg)

### Steps to attack:
1. Login to the target application with admin privileges.
2. Click at the gear icon in the upper right corner.
3. Select "Branding" menu.
4. At Favicon, click "Select File".
5. Browse the file where we prepared the payload XSS.
6. Click "Save".
7. After found a success message select "Branding" menu again.
8. Right click and select "Open Image in New Tab", it will show that the payload XSS was executed.

### Discoverer:
:shipit: Grim The Ripper Team by SOSECURE Thailand

### Medium:
- https://grimthereaperteam.medium.com/snipe-it-version-v6-0-2-file-upload-cross-site-scripting-b15becc1a5ea

### Disclosure Timeline:
- 2022–05–27: Vulnerability discovered.
- 2022–05–27: Vulnerability reported to the MITRE corporation.
- 2022–05–27: Public disclosure of the vulnerability.
- 2022–07–08: CVE has been reserved.

Reference:
1. https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-34963
2. https://github.com/bypazs/CVE-2022-32060
3. https://snipeitapp.com
4. https://github.com/snipe/snipe-it/releases/tag/v6.0.2
