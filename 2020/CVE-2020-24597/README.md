# Made by HK
# CVE-2020-24597: Directory traversal in com_media to RCE
# Note: Because Joomla core 3.9.21 fixed improperly, therefore this bug has't patched improperly. I can bypass this patch eseaily. I want to keep this secret until this bug will have been fixed completely.
# Link
https://developer.joomla.org/security-centre/827-20200803-core-directory-traversal-in-com-media.html
# PoC (Full)
## Affected version: Joomla core <=3.9.24
## User requirement: Admin account (Not Superadmin)
## Gain access: Create superadmin, then trigger RCE.
## Remote Code Execution (RCE) in Joomla
## Run *cve202024597.py* with your credentials and access link rce:
#python cve202024597.py -url http://test.local -u admin -p 1234 -rce 1

![image](https://user-images.githubusercontent.com/24661746/91253221-8cfabd80-e789-11ea-9a0b-da2ec5975653.png)

Full PoC in here:

https://github.com/HoangKien1020/CVE-2021-23132
