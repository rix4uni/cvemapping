
# CVE-2024-34361 Pi-hole Remote Code Execution (SSRF to RCE)

## Description
This repository contains an exploit for CVE-2024-34361, a critical vulnerability (CVSS 8.6) discovered in Pi-hole, a DNS sinkhole widely used to block advertisements and tracking domains at the network level.

The vulnerability arises from improper validation of URLs, which can be exploited via SSRF (Server-Side Request Forgery). Under certain conditions, this SSRF can be escalated to RCE (Remote Code Execution) using the Gopherus protocol.

Exploiting this vulnerability allows an attacker to send arbitrary requests from the Pi-hole server, potentially leading to unauthorized execution of commands on the system.

This security flaw not only compromises the confidentiality and integrity of the system but also poses a significant threat to its availability by allowing an attacker to execute arbitrary commands.

Affected Versions:
- Pi-hole version <=5.18.2, with the issue resolved in version 5.18.3.

## Installation
Ensure Python is installed on your system to utilize this exploit. Clone the repository and set up the necessary environment as follows:

```bash
git clone https://github.com/T0X1Cx/CVE-2024-34361-Pi-hole-SSRF-to-RCE.git
cd CVE-2024-34361-Pi-hole-SSRF-to-RCE
pip install -r requirements.txt
```

## Usage
Execute the exploit using the command below:

```bash
python3 exploit.py [Pi-Hole URL] [Admin password]
```

### Installing Redis for Exploit

To use this exploit, you need to install and configure Redis on the target system. Follow these steps to install Redis:

1. Download and extract Redis:
    ```bash
    wget https://download.redis.io/releases/redis-6.0.3.tar.gz
    tar -xvf redis-6.0.3.tar.gz
    cd redis-6.0.3
    ```

2. Compile and start Redis:
    ```bash
    make
    cd src/
    sudo ./redis-server
    ```

## Proof of Concept

![image](https://github.com/T0X1Cx/CVE-2024-34361-Exploit/assets/71453093/aade022c-99e8-4179-a55b-8bde65572bd4)

![image](https://github.com/T0X1Cx/CVE-2024-34361-Exploit/assets/71453093/7345d316-7bed-40e7-818d-a63e3a0ebd03)


## Disclaimer
This exploit is for educational and ethical security testing purposes only. The use of this exploit against targets without prior mutual consent is illegal, and the developer disclaims any liability for misuse or damage caused by this exploit.

## Credits
Exploit developed by Julio Ángel Ferrari (Aka. T0X1Cx)
