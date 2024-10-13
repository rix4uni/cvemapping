# CVE-2018-19422-SubrionCMS-RCE

SubrionCMS 4.2.1 Authenticated Remote Code Execution

- /panel/uploads in Subrion CMS 4.2.1 allows remote attackers to execute arbitrary PHP code via a .pht or .phar file, because the .htaccess file omits these. 

### Exploit Usage

#### Commands:
- Windows/Linux:
`$ sudo python3 subrionRCE.py -u http://IP/panel/ -l <user> -p <password>  `

![](https://github.com/hevox/CVE-2018-19422-SubrionCMS-RCE/blob/main/imgs/SubrionPOC.png)

- References:

  https://www.exploit-db.com/exploits/49876
  
  https://packetstormsecurity.com/files/162591/Subrion-CMS-4.2.1-Shell-Upload.html
  
  https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-19422
