# CVE-2024-32651 changedetection < 0.45.20 - Remote Code Execution (RCE)

Server-Side Template Injection Exploit!!
## 1. Title
Remote Code Execution via Server-Side Template Injection (SSTI) in Vulnerable Web Application

## 2. Description
This exploit targets a web application vulnerable to Server-Side Template Injection (SSTI). By exploiting this vulnerability, an attacker can execute arbitrary commands on the server. The provided Python script automates the exploitation process by submitting a payload that triggers a reverse shell.

## 3. Vulnerability Information
1. **CVE ID:** CVE-2024-32651
2. **Affected Systems:** Web applications that use Server-Side Template Injection (SSTI) and have a vulnerable configuration.

## 4. Proof of Concept
To reproduce the vulnerability, execute the provided Python script against the vulnerable web application. Ensure that you have a listener (e.g., `nc -lvp 9999`) running to capture the reverse shell connection.

## 5. Usage
1. **Save the script** to a file named `CVE-2024-32651.py`.

2. **Install the required Python libraries** if not already installed:
   ```bash
   pip install requests beautifulsoup4

3.  To use the script, provide the following command-line arguments:
- `--url`: **Base URL of the vulnerable web application** (e.g., `http://10.10.10.10:5000`).
- `--port`: **Port for the listener** (e.g., `9999`).
- `--ip`: **IP address of the listener** (e.g., `10.10.50.22`).
- `--notification`: *(Optional)* **Notification URL** if you want to use a specific notification URL.
- 
4. **Run the script** using Python 3 with the required arguments. The syntax is:
   ```bash
   python3 CVE-2024-32651.py --url http://<TARGET_URL> --port <LISTENER_PORT> --ip <LISTENER_IP> [--notification <NOTIFICATION_URL>]

## 6. Credits
This fixed version of the exploit was based on an original exploit published by Zach Crosman (zcrosman) with EDB-ID: 52027. You can view the original exploit [here](https://www.exploit-db.com/exploits/52027).
I  thank Zach Crosman for his contribution to the security community.
