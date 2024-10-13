
# SolarWinds-CVE-2021-35250
![solarwinds-inc-logo835x396-702x336](https://user-images.githubusercontent.com/37665001/231947256-789b2a70-cba1-45d1-85db-27e07efe68c8.jpg)
### Serv-U [v.15.3.0.X] CVE-2021-35250-Directory-Traversal 
Hello everyone

This is my first POC, don't judge strictly.

### **Disclaimer**
The author of this repository is not responsible for any damage caused by the use or misuse of these PoC exploits. These PoCs are intended for educational and research purposes only, and should never be used to target or exploit systems without explicit permission from the owner.

### Description
I work for the "R-X Team". During penetration testing, I came across Serv-U. I started looking for known vulnerabilities, and I was interested in CVE-2020-27994. But it was closed by an update in version 15.2.2, and I was working with Serv-U version 15.3.0. "I decided to dig deeper and modify the payload in various ways, as well as modify the HTTP request itself, after much agony I managed to reproduce the vulnerability of directory traversal" :)

 The vulnerability allows a remote user to perform directory traversal attacks by sending a specially crafted HTTP request and reading arbitrary files in the system.
Reading files is only possible on the C:
\ drive, an attacker can get information on the file server only by knowing the path to the files. There are 3 known options for which files and how an attacker can read:
- Default Windows files. Example: "C:\Windows\win.ini ";
- Brute force file detection;
- Determination of file paths in default Windows files or used software on the server.

POC:


![Serv-U](https://user-images.githubusercontent.com/37665001/231661246-19fdf7a2-326c-4226-af72-f82af36bbbf4.png)
![Serv-U1](https://user-images.githubusercontent.com/37665001/231953431-95dd3276-6c77-4b2f-9ebe-d63bfedad37f.png)

### **Recommendations:**
https://nvd.nist.gov/vuln/detail/CVE-2021-35250

https://support.solarwinds.com/SuccessCenter/s/article/Serv-U-15-3-HotFix-1?language=en_US

https://www.solarwinds.com/trust-center/security-advisories/cve-2021-35250




