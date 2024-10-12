# FortiGate cve-2024-21762-checker
This script is used to check for vulnerabilities in Fortigate SSL VPNs based on CVE-2024-21762. It uses Shodan to find vulnerable devices and test their vulnerability.

## Features
- Uses Shodan API to find Fortigate devices running SSL VPN on port 10443.
- Checks the vulnerability status of the devices.
- Flexible shodan queries
- Displays the result with additional information such as organization and country.

## Requirements
- Python 3.x
- Shodan API Key

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/rdoix/cve-2024-21762-checker.git
    cd cve-2024-21762-checker
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set Shodan API Key as an environment variable:
    ```bash
    export SHODAN_API_KEY="YOUR_SHODAN_API_KEY"
    ```

## Usage
Run the script with the following command:
```bash
python3 cve-2024-21762-checker.py
```

## Example Output
```
1.1.1.1 | ABC Company | Indonesia | Vulnerable
1.1.2.2 | XYZ Corporation | United States | Patched
```
