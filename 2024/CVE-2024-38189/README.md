# 🔥 PoC for CVE-2024-38189 🔥

![Educational Purpose Only](https://img.shields.io/badge/educational-purpose%20only-orange)
![CVE-2024-38189](https://img.shields.io/badge/critical-red)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)

## ⚠️ Disclaimer

**This Proof-of-Concept (PoC) is provided for educational purposes only.**  
This exploit was **NOT** discovered by me and should be used only in controlled environments for learning or authorized testing. Unauthorized use of this script on systems without permission is illegal and unethical.

## 🚀 Overview

This repository contains a Python script demonstrating an advanced exploitation technique for **CVE-2024-38189**. This vulnerability allows an attacker to execute arbitrary code remotely. The exploit uses various methods to achieve obfuscation, persistence, and secure communication with a command and control (C2) server.

## 📜 Features

### ✨ Advanced Obfuscation
The script employs AES-256 encryption and XOR techniques to obfuscate the payload, making detection by security tools more difficult.

### 🔁 Metamorphic Payloads
Generates dynamic and varied payloads each time the script runs, reducing the risk of detection by signature-based security systems.

### 🧩 Stealth Persistence
The script includes multiple methods to establish persistence on the target system while avoiding detection, including the use of Windows Task Scheduler and registry modifications.

### 🕵️‍♂️ Virtualization Detection
Incorporates advanced techniques to detect if the script is running in a virtualized or sandboxed environment, exiting immediately if so.

### 🔒 Secure C2 Communication
Establishes a secure communication channel between the infected system and the attacker's server, allowing encrypted command execution and data exfiltration.

## 📝 Vulnerability Details

- **Impact**: Remote Code Execution
- **Max Severity**: Important
- **Weakness**: 
  - CWE-20: Improper Input Validation
- **CVSS Source**: Microsoft
- **CVSS**: 3.1 8.8 / 8.2
- **Attack Vector**: Network
- **Attack Complexity**: Low
- **Privileges Required**: None
- **User Interaction**: Required
- **Scope**: Unchanged
- **Confidentiality**: High
- **Integrity**: High
- **Availability**: High
- **Exploit Code Maturity**: Functional
- **Remediation Level**: Official Fix
- **Report Confidence**: Confirmed

## 🛡️ How the Exploit Works

### Elevation of Privilege

Elevation of privilege is a security vulnerability where an attacker can gain unauthorized access to sensitive data or systems. This specific vulnerability, **CVE-2024-38189**, affects multiple Microsoft products, including:

- Windows 10 and later versions
- Windows Server 2019 and later versions
- Office 365 and earlier versions

An attacker can exploit this vulnerability by sending a specially crafted file, such as a document or spreadsheet, to an affected system. Upon opening the file, the malicious code is executed, potentially leading to the execution of arbitrary code with elevated privileges.

### Why CVE-2024-38189 is Critical

1. **Elevation of Privilege**: Attackers can gain unauthorized access to sensitive data or systems.
2. **Remote Exploitability**: Can be exploited remotely, making it easier for attackers to target systems without physical access.
3. **Widespread Impact**: Affects widely used Microsoft products across various industries.

## 🔧 Mitigation

To mitigate the risks associated with CVE-2024-38189, consider the following steps:

- **Update Your Systems**: Ensure your systems are up-to-date with the latest security patches from Microsoft.
- **Use a Firewall**: Block incoming connections from unknown or untrusted sources.
- **Implement File Filtering**: Configure rules to prevent malicious files from being executed.
- **Monitor for Suspicious Activity**: Regularly monitor systems and networks for unusual activity.

## 🛠️ Usage

**IMPORTANT**: This script should be run in a controlled environment, such as a virtual machine, and with the proper authorization. Unauthorized use is illegal and unethical.

```bash
# Clone the repository
git clone https://github.com/vx7z/CVE-2024-38189.git

# Change directory
cd cve-2024-38189-poc

# Install required dependencies
pip install -r requirements.txt

# Run the script
python3 exploit.py
