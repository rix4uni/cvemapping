# CVE-2021-44909

## Exploit Title: orangescrum 1.8.0 - Remote Command Execution RCE (unauthenticated)
- Date: 03/12/2021
- Vendor Homepage: [https://www.orangescrum.org/](https://www.orangescrum.org/)
- Software Link: [https://github.com/Orangescrum/orangescrum](https://github.com/Orangescrum/orangescrum)
- Version: 1.8.0
- Tested on: Windows 10 x64 using XAMPP 7.4.23, Apache/2.4.48 (Win64) OpenSSL/1.1.1l PHP/7.4.2

### Exploit Steps:
1. Open http://localhost/orangescrum/install/index.php
2. Craft your malicious PHP file
3. Compress and upload the previous PHP file under the name "AddonInstaller-V1.6.zip"
4. Ignore received errors and open http://localhost/orangescrum/install/files/
5. Locate and call your PHP file
6. Receive your shell
