# CVE-2011-2523 - vsftpd 2.3.4 Exploit


## Description
- vsftpd, which stands for `Very Secure FTP Daemon`,is an FTP server for Unix-like systems, including Linux. It is licensed under the GNU General Public License. It supports IPv6 and SSL.

- In July 2011, it was discovered that vsftpd version 2.3.4 downloadable from the master site had been compromised.  Users logging into a compromised vsftpd-2.3.4 server may issue a `:)` smileyface as the username and gain a command shell on port `6200`.  This was not an issue of a security hole in vsftpd, instead, someone had uploaded a different version of vsftpd which contained a backdoor. Since then, the site was moved to Google App Engine.


## Requirements

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
pip install argparse
```

## Installation

```bash
git clone https://github.com/padsalatushal/CVE-2011-2523.git
cd ./CVE-2011-2523
chmod +x exploit.py
```


## Usage

python3 exploit.py -host Target_IP 

**Example :** python3 exploit.py -host 192.168.168.128


![image](https://user-images.githubusercontent.com/57517785/140640932-aa2e2a7f-cf09-44b1-a3f9-ce97bfa28f00.png)


## Test

You can test the exploit on [Metasploitable2](https://sourceforge.net/projects/metasploitable/files/Metasploitable2/)

## Resources 

https://www.computersecuritystudent.com/SECURITY_TOOLS/METASPLOITABLE/EXPLOIT/lesson8/index.html
https://subscription.packtpub.com/book/networking_and_servers/9781786463166/1/ch01lvl1sec18/vulnerability-analysis-of-vsftpd-2-3-4-backdoor
