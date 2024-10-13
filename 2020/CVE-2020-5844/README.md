# Exploit for CVE-2020-5844 (Pandora FMS v7.0NG.742) - Remote Code Execution

![GitHub CVE Cover](https://user-images.githubusercontent.com/23003787/172497977-d6f22c52-ba5d-4fa0-9c90-04fc685ad871.png)

**Like this repo? Give us a ⭐!**

*For educational and authorized security research purposes only.*

## Exploit Author
[@UNICORDev](https://unicord.dev) by ([@NicPWNs](https://github.com/NicPWNs) and [@Dev-Yeoj](https://github.com/Dev-Yeoj))

## Vulnerability Description
`index.php?sec=godmode/extensions&sec2=extensions/files_repo` in Pandora FMS v7.0 NG allows authenticated administrators to upload malicious PHP scripts, and execute them via base64 decoding of the file location. This affects `v7.0NG.742_FIX_PERL2020`.

## Exploit Description
Use this exploit for remote code execution on vulnerable versions of Pandora FMS. Requires a target IP address and port. Requires valid username/password or valid PHPSESSID cookie authentication. Run in default mode to upload a basic PHP web shell. Run in custom command mode to run a custom command on the target. Run in reverse shell mode to receive a reverse shell from the target on a listener you set up. Run in web shell custom mode to change the name of the PHP web shell file.

## Usage
```bash
  python3 exploit-CVE-2020-5844.py -t <target-IP> <target-port> -u <username> <password>
  python3 exploit-CVE-2020-5844.py -t <target-IP> <target-port> -p <PHPSESSID>
  python3 exploit-CVE-2020-5844.py -t <target-IP> <target-port> -p <PHPSESSID> [-c <custom-command>]
  python3 exploit-CVE-2020-5844.py -t <target-IP> <target-port> -p <PHPSESSID> [-s <local-ip> <local-port>]
  python3 exploit-CVE-2020-5844.py -t <target-IP> <target-port> -p <PHPSESSID> [-w <name.php>]
  python3 exploit-CVE-2020-5844.py -h
```

## Options
```bash
  -t    Target host and port. Provide target IP address and port.
  -u    Target username and password. Provide username and password to log in to Pandora FMS.
  -p    Target valid PHP session ID. No username or password needed. (Optional)
  -s    Reverse shell mode. Provide local IP address and port. (Optional)
  -c    Custom command mode. Provide command to execute. (Optional)
  -w    Web shell custom mode. Provide custom PHP file name. (Optional)
  -h    Show this help menu.
```

## Download
[Download exploit-CVE-2020-5844.py from GitHub](https://raw.githubusercontent.com/UNICORDev/exploit-CVE-2020-5844/main/exploit-CVE-2020-5844.py)

[Download exploit-CVE-2020-5844.py from ExploitDB](https://www.exploit-db.com/exploits/50961)

### Searchsploit (ExploitDB)
```bash
searchsploit -u
searchsploit -m 50961
```

## Applies To
Pandora FMS v7.0NG.742

## Exploit Requirements
- python3
- python3:requests

## Demos
### Default Mode with Username and Password
![default](https://user-images.githubusercontent.com/23003787/169666284-9928f915-4b07-49b0-a835-8b28cbbb9ed3.gif)

### Default Mode with PHPSESSID
![default_sess](https://user-images.githubusercontent.com/23003787/169666223-de66bc05-f4fb-44d7-af79-e515d13fb25d.gif)

### Custom Command Mode
![command](https://user-images.githubusercontent.com/23003787/169666226-d9b8ee5f-81fa-4e34-b498-9c817d2bdb40.gif)

### Reverse Shell Mode
![shell](https://user-images.githubusercontent.com/23003787/169666229-cbf1e366-4c92-4aa7-a8b5-e250fbf8caf8.gif)

### Custom Web Shell Name Mode
![web](https://user-images.githubusercontent.com/23003787/169666230-fce0e884-2163-40f5-a418-afa6adbe45e8.gif)

## Credits
- https://nvd.nist.gov/vuln/detail/CVE-2020-5844
- https://sourceforge.net/projects/pandora/files/Pandora%20FMS%207.0NG/742_FIX_PERL2020/Tarball/pandorafms_server-7.0NG.742_FIX_PERL2020.tar.gz
- https://app.hackthebox.com/machines/Pandora
- https://github.com/TheCyberGeek/CVE-2020-5844
- https://github.com/shyam0904a/Pandora_v7.0NG.742_exploit_unauthenticated
- https://www.exploit-db.com/exploits/50961
