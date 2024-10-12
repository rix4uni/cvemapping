# CVE-2024-26304 - Remote Code Execution Vulnerability in ArubaOS

## Overview

**CVE-2024-26304** is a critical remote code execution (RCE) vulnerability affecting **ArubaOS** due to a buffer overflow in its L2/L3 Management service. An attacker can exploit this by sending specially crafted packets to the **PAPI** (Process Application Programming Interface) UDP port **8211**, resulting in the execution of arbitrary code with elevated privileges.

### CVSS Score: 9.8 (Critical)
- **Attack Vector**: Network
- **Attack Complexity**: Low
- **Privileges Required**: None
- **User Interaction**: None
- **Confidentiality Impact**: High
- **Integrity Impact**: High
- **Availability Impact**: High

## Affected Products

- ArubaOS systems with vulnerable versions
- Systems using the **PAPI UDP port 8211**

Refer to [Aruba's official advisory](https://www.arubanetworks.com/assets/alert/ARUBA-PSA-2024-004.txt) for details on affected versions.

## Exploitation

An unauthenticated remote attacker can exploit this vulnerability by sending malicious packets to the PAPI UDP port. Successful exploitation results in arbitrary code execution, enabling the attacker to take complete control over the device.

### Proof-of-Concept (PoC)

A proof-of-concept exploit is available for this vulnerability. The exploit script `CVE-2024-26304.py` demonstrates how an attacker can leverage the vulnerability to execute code on the target system.

## How to Use the Exploit Tool

The tool `CVE-2024-26304.py` is a proof-of-concept exploit script designed to demonstrate this vulnerability. Here’s how to run it:

### Prerequisites

- Python 3.x
- Required Python libraries (if any, listed in `requirements.txt`)

## Parameters
- target: The IP address of the vulnerable ArubaOS device.
- port: (Optional) The PAPI UDP port (default: 8211).

### Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/CVE-2024-26304
   cd CVE-2024-26304
   pip install -r requirements.txt
   python CVE-2024-26304.py --target <target_ip> --port 8211

## Disclaimer
This tool is intended for educational purposes and penetration testing within environments where you have explicit permission. Misuse of this tool can result in criminal charges or fines. The authors are not responsible for any misuse.
