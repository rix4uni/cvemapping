# CVE-2024-25641 RCE for Cacti 1.2.26

This repository automates the process of exploiting CVE-2024-25641 on Cacti 1.2.26.
When a user is authenticated, An arbitrary file write vulnerability, exploitable through the "Package Import" feature, allows authenticated users having the "Import Templates" permission to execute arbitrary PHP code on the web server (RCE).
Original report: https://github.com/Cacti/cacti/security/advisories/GHSA-7cmj-g5qc-pj88

## Features

- **Automatic Exploitation**: Easily execute the exploit with minimal setup.
- **Customizable Target**: Quickly configure the URL, username, password, and payload.
- **Dependency Management**: Ensure all necessary packages are installed with a single command.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system
- Internet connection to download dependencies

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/5ma1l/CVE-2024-25641.git
   cd CVE-2024-25641
2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt

## Usage

1. **Prepare your PHP payload:**

    By default, the script uses ./php/monkey.php as the payload.
    Make sure to modify the IP address and port inside the PHP payload file if needed.

2. **Run the exploit:**
    ```bash
    python3 exploit.py <URL> <username> <password> [-p <payload_path>]

## Arguments

- **URL**: The target Cacti URL.
- **username**: Login username.
- **password**: Login password.
- **-p/--payload**: Path to the PHP payload file (default: `./php/monkey.php`).

## Execute the payload:

After the script successfully uploads the payload, you can choose to execute it directly from the script or manually through the browser.

## Disclaimer

    This tool is intended for educational purposes only. Unauthorized use of this tool against systems without explicit permission is illegal and unethical. The author is not responsible for any misuse or damage caused by this tool.
