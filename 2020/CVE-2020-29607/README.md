# CVE-2020-29607-Exploit
### Exploit Title: Pluck CMS 4.7.13 - File Upload Remote Code Execution (Authenticated)

## CVE description:
A file upload restriction bypass vulnerability in Pluck CMS before 4.7.13 allows an admin privileged user to gain access in the host through the "manage files" functionality, which may result in remote code execution.
  - https://nvd.nist.gov/vuln/detail/CVE-2020-29607

## ExploitDB:
  - https://www.exploit-db.com/exploits/49909

## Exploit Description:
An authenticated attack can upload a .phar file by using http://IP/admin.php?action=files to gain a webshell.
- Vendor Homepage: Vendor Homepage: https://github.com/pluck-cms/pluck
- Software Link: https://github.com/pluck-cms/pluck/releases/tag/4.7.13
- Version: 4.7.13
- Tested on Xubuntu 20.04

## Usage:
python3 exploit.py Target_IP Target_Port Username



- 🕊️ Twitter: [@0xAbbarhSF](https://twitter.com/0xAbbarhSF)
[![Tweet](https://img.shields.io/twitter/url/http/0xAbbarhSF.svg?style=social)](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fdeveloper.twitter.com%2Fen%2Fdocs%2Ftwitter-for-websites%2Ftweet-button%2Foverview&ref_src=twsrc%5Etfw&text=CMS-Xploiter%20-%20Automated%20Pentest%20Recon%20Scanner%20%400xAbbarhSD&tw_p=tweetbutton&url=https%3A%2F%2Fgithub.com%2F0xAbbarhSF%)
