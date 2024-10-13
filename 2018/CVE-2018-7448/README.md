# exploit-cve-2018-7448

### Purpose
This is a python script to automate CMS Made Simple 2.1.6 - Remote Code Execution - CVE-2018-7448.

It was created based on https://www.exploit-db.com/exploits/44192.

### Usage
```bash
python3 exploit-CVE-2018-7448.py -t 127.0.0.1/cmsms -d cms -u root -p password
```

### Troubleshooting
If the installer is different from `cmsms-2.1.6-install.php`, you will have to change the file name in the code.

The exploit works on HTTP by default, if you need to exploit HTTPS, change the URLs in the code.
