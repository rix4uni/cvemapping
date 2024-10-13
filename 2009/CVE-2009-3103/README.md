# Microsoft-Windows---srv2.sys-SMB-Code-Execution-Python-MS09-050-
Microsoft Windows - 'srv2.sys' SMB Code Execution (Python) (MS09-050)

# Exploit for CVE-2009-3103

## Overview

This Python script is an updated version of a public exploit for CVE-2009-3103. The original code relied on the SMB.connection module, which has been replaced in this version to make the script more versatile and compatible.

## Description

The exploit targets a specific vulnerability (CVE-2009-3103) and injects a payload into a target system, triggering an authentication event to execute the payload.

## Usage

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Run the exploit script with the target IP:

    ```bash
    python exploit.py <target-ip>
    ```

## Disclaimer

This script is provided as-is and for educational purposes. Be aware of the legal implications of using such tools in unauthorized environments. Use responsibly and with proper authorization.

## Credits

Original exploit source: [Original Exploit]([https://github.com/ohnozzy/Exploit](https://www.exploit-db.com/exploits/40280))

## License

This project is licensed under the [MIT License](LICENSE).
