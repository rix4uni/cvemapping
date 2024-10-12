# CVE-2024-3273 - D-Link Remote Code Execution (RCE) Exploit

## Description
This repository contains an exploit for **CVE-2024-3273**, a critical vulnerability found in specific D-Link devices that allows for Remote Code Execution (RCE). The vulnerability arises from improper input validation in the `nas_sharing.cgi` CGI scripts, enabling attackers to execute arbitrary commands without authentication.

## Impact
Exploitation of CVE-2024-3273 can grant unauthorized access to affected devices, allowing attackers to:
- Manipulate system configurations
- Access sensitive data
- Deploy malicious code

## Affected Products
This vulnerability primarily impacts various D-Link NAS devices and potentially other products utilizing the vulnerable CGI scripts.

## Usage
To use the exploit, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/X-Projetion/CVE-2024-3273-EXPLOIT.git
   cd CVE-2024-3273-EXPLOIT
2. Ensure you have the necessary dependencies installed:
   pip install -r requirements.txt
3. Execute the exploit:
   python CVE-2024-3273.py -u <target_url>

## Mitigation
Users are strongly advised to:
- Update their D-Link devices to the latest firmware to patch the vulnerability.
- Implement network segmentation to isolate vulnerable devices.
- Monitor network traffic for suspicious activity.

## Disclaimer
This exploit is intended for educational and research purposes only. Use responsibly and ensure compliance with all applicable laws and regulations. I do not take any responsibility for the misuse of this exploit or any consequences resulting from its use.

## Contributing
Feel free to contribute by submitting issues or pull requests to improve the documentation or functionality of the exploit.
