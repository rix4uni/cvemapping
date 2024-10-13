# Exploit for Jenkins serialization vulnerability - CVE-2016-0792

---
[https://www.exploit-db.com/exploits/42394/](https://www.exploit-db.com/exploits/42394/)

#### More information can be found here

1. [Contrast Security](https://www.contrastsecurity.com/security-influencers/serialization-must-die-act-2-xstream)

2. [Pentester Lab](https://www.pentesterlab.com/exercises/cve-2016-0792/)

#### Requirements

1. Python 3.6.x

2. [requests](http://docs.python-requests.org/en/master/) library is required for this exploit to work

      `sudo pip install requests`

#### Usage
- [Old way](https://github.com/jpiechowka/jenkins-cve-2016-0792)
- New Way
```bash
python3 exp.py -u <url> -c <command>    
```
```bash
usage: exploit.py [-h] [-u U] [-c C]

CVE-2016-0792

optional arguments:
  -h, --help  show this help message and exit
  -u U        url to exploit
  -c C        command to execute
```
![](images/1.png)

  


#### Disclaimer
Using this software to attack targets without permission is illegal. I am not responsible for any damage caused by using
 this software against the law.