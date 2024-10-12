# RADIUS Vulnerability Detector

**Limits of the Code:**

The code is aimed directly at detecting MD5 conflict. However, a more comprehensive analysis may be required to thoroughly test all aspects of CVE-2024-3596.
This code can only detect attacks based on MD5 collision. Additional analysis may be required to detect other potential vulnerabilities (for example, TLS or IPSec deficiencies).

<p><a href="https://www.linkedin.com/in/alperen-ugurlu/">Alperen Ugurlu</a></p>
<picture>
  <source srcset="https://github-readme-stats.vercel.app/api?username=alperenugurlu&show_icons=true&theme=dark" media="(prefers-color-scheme: dark)" />
  <source srcset="https://github-readme-stats.vercel.app/api?username=alperenugurlu&show_icons=true" media="(prefers-color-scheme: light), (prefers-color-scheme: no-preference)" />
  <img src="https://github-readme-stats.vercel.app/api?username=alperenugurlu&show_icons=true" />
</picture>
```


![Python](https://img.shields.io/badge/python-v3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange)


This script detects the **CVE-2024-3596** vulnerability in RADIUS/UDP traffic by checking for MD5 collisions. It captures RADIUS Access-Request packets and attempts to generate MD5 collisions to determine if the system is vulnerable.

## Features

- **Real-time packet analysis**: Capture and analyze RADIUS packets on the fly.
- **MD5 collision detection**: Identify potential vulnerabilities using advanced cryptographic techniques.
- **User-friendly**: Simple to set up and use with clear prompts for necessary inputs.

## Requirements

- Python 3.x
- `scapy` library
- `pyrad` library

## Installation

1. Ensure you have Python 3 installed. You can check your Python version with:
    ```bash
    python3 --version
    ```

2. Install the necessary libraries:
    ```bash
    pip3 install scapy pyrad
    ```

## Usage

1. Save the script to a file, for example `radius_vulnerability_detector.py`.

2. Run the script:
    ```bash
    python3 radius_vulnerability_detector.py
    ```

3. Provide the necessary inputs when prompted:
   - **Shared secret**: The shared secret between the RADIUS server and clients.
   - **Network interface**: The network interface to listen on (e.g., `eth0`).
   - **RADIUS dictionary path**: The full path to your RADIUS dictionary file.

The script will capture RADIUS Access-Request packets and analyze them for MD5 collisions. If a collision is detected, it will indicate that your system may be vulnerable to CVE-2024-3596.

Vulnerable Authentication Methods
PAP (Password Authentication Protocol)
CHAP (Challenge-Handshake Authentication Protocol)
MS-CHAPv2 (Microsoft Challenge-Handshake Authentication Protocol version 2)
Other non-EAP authentication methods

**Secure Systems and Methods**
802.1X
IPSec
TLS
Eduroam
OpenRoaming



**Motivation**
With the increasing sophistication of cyber threats, it's critical to ensure that authentication protocols like RADIUS are secure. This project was developed to provide network administrators with a tool to identify and mitigate potential vulnerabilities in their RADIUS implementations.

**How it Works**
The script listens for RADIUS Access-Request packets and performs a cryptographic analysis to detect MD5 collisions. If a vulnerability is found, it provides a warning to the user, allowing for timely security measures to be taken.

**Future Enhancements**
Support for additional protocols: Extend the detection capabilities to other authentication protocols.
Automated remediation suggestions: Provide actionable steps for mitigating detected vulnerabilities.
Integration with SIEM systems: Allow for real-time monitoring and alerting in enterprise environments.

**License**
This project is licensed under the MIT License - see the LICENSE file for details.

**Disclaimer**
This script is intended for educational and testing purposes only. Use it responsibly and only on systems you own or have explicit permission to test. Unauthorized use of this script on networks and systems that you do not own is illegal and unethical.

**Contributing**
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

**Acknowledgements**
Special thanks to the researchers who discovered the CVE-2024-3596 vulnerability and inspired this detection script.

