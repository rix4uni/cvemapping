# CVE-2023-32707
An improved POC exploit based on the reported CVE on [exploitdb](https://www.exploit-db.com/exploits/51747)

Exploit Title: Splunk 9.0.5 - Admin Account Takeover
CVE: CVE-2023-32707

## Overview

This script allows for exploiting a vulnerability in Splunk 9.0.5, leading to admin account takeover. The exploit leverages a low-privilege user with the `edit_user` capability to escalate privileges.

## Prerequisites

- Python 3.x
- Required Python packages (install using `pip3 install -r requirements.txt`):
  - requests
  - urllib3

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/9xN/CVE-2023-32707.git
    cd CVE-2023-32707
    ```

2. Run the script with the required parameters:

    ```bash
    python3 exploit.py --host <splunk_host> --username <splunk_username> --password <splunk_password> --target-user <target_user> --force-exploit
    ```

    Replace `<splunk_host>`, `<splunk_username>`, `<splunk_password>`, and `<target_user>` with your Splunk server details.

## Command-line Options

- `--host`: Splunk host or IP address (required)
- `--username`: Splunk username (required)
- `--password`: Splunk password (required)
- `--target-user`: Target user for account takeover (required)
- `--force-exploit`: Force the exploit (optional)
- `--proxy-file`: File containing proxy settings (optional)

## Proxies

To use proxies, specify the `--proxy-file` with the path to a file containing proxy settings.

Example:

```bash
python3 exploit.py --host <splunk_host> --username <splunk_username> --password <splunk_password> --target-user <target_user> --force-exploit --proxy-file proxies.txt
```
