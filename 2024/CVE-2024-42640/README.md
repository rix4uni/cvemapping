# CVE-2024-42640

<br><br> 
<div align="center">
  <img width="250" src="https://zyenra.com/assets/img/angular-bug-tp.png" alt="angular-bug"> <br> <br>
  <p>CVE-2024-42640 <br>
  <b>Unauthenticated Remote Code Execution via Angular-Base64-Upload Library</b> <br>
  for more details: <b><a href="https://www.zyenra.com/blog/unauthenticated-rce-in-angular-base64-upload.html"> blog </a></b>
  </p>
</div>

### Introduction 

`angular-base64-upload` versions prior to v0.1.21 are vulnerable to unauthenticated remote code execution via the `angular-base64-upload/demo/server.php` endpoint. Exploiting this vulnerability allows an attacker to upload arbitrary file content to the server, which can subsequently be accessed through the angular-base64-upload/demo/uploads endpoint. This lead to the execution of previously uploaded content and ultimately enable the attacker to achieve code execution on the server.


![alt text](https://www.zyenra.com/assets/img/angular-base64-upload-rce-poc.png)

<br>

### Usage 

```bash
git clone https://github.com/rvizx/CVE-2024-42640
cd CVE-2024-42640
python3 exploit.py <target>
```

<br>

### Security Issue Details 

Exploit Title: Unauthenticated RCE via Angular-Base64-Upload Library <br>
Researcher: Ravindu Wickramasinghe | rvz (@rvizx9) <br>
Severity: Critical - 10.0 (CVSS 4.0) <br>
Vendor Homepage: https://www.npmjs.com/package/angular-base64-upload <br>
Software Link: https://github.com/adonespitogo/angular-base64-upload <br>
Vector: CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H <br>
Vulnerable Versions: < v0.1.21 <br>
Fixed Versions: >= v0.1.21 <br>
Tested on: Arch Linux <br>
CVE : CVE-2024-42640 <br>
NIST: https://nvd.nist.gov/vuln/detail/CVE-2024-42640 <br>
Github PoC Exploit Link : https://github.com/rvizx/CVE-2024-42640 <br>
Blog Post: https://www.zyenra.com/blog/unauthenticated-rce-in-angular-base64-upload.html <br>
