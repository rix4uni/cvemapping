# PoC for CVE-2023-32749

This is a quick and dirty PoC I wrote for CVE-2023-32749 for Pydio Cells. The scripts creates a new user account with the all the roles available when provided with a valid credential.  

All credits goes to the original researchers.


# Installation

The only requirements is the requests package from python to make the web requests. If it is not installed on your system then it can be done with

```bash
pip3 install -r requirements.txt
```


# Usage

```plaintext
exploit.py [-h] -u USER -p PASSWORD -l URL

PoC for PyDio Cells - CVE-2023-32749

options:
  -h, --help            show this help message and exit
  -u USER, --user USER
  -p PASSWORD, --password PASSWORD
  -l URL, --url URL
```


## References

- https://packetstormsecurity.com/files/172645/Pydio-Cells-4.1.2-Privilege-Escalation.html
- https://pydio.com/en/docs/developer-guide/rest-api

Again all credits goes to the original PoC at RedTeam Pentesting GmbH

## Disclamer
The usage of this script is at the user's own risk. The author shall not be held responsible for any damages or misuse of this script. It is the user's responsibility to ensure that the script is used in compliance with all applicable laws and regulations.





