# LiteSpeed Cache Privilege Escalation PoC - CVE-2024-28000

This repository contains a Proof of Concept (PoC) script for exploiting a privilege escalation vulnerability in the LiteSpeed Cache WordPress plugin. The vulnerability, identified as **CVE-2024-28000**, allows unauthenticated users to gain Administrator-level access to a WordPress site by brute-forcing a weak security hash used in the plugin.

## Vulnerability Overview

The LiteSpeed Cache plugin's user simulation feature is protected by a weak security hash generated using predictable values. An attacker can exploit this vulnerability by brute-forcing the security hash and passing it in a cookie along with a targeted user ID. If successful, the attacker can escalate their privileges to that of an Administrator.

### Affected Versions

* LiteSpeed Cache plugin versions prior to 6.4 are vulnerable.

### Author
- PoC: Alucard0x1
- Telegram: [https://t.me/Alucard0x1](https://t.me/Alucard0x1)

### Credit
- Bug Founder: John Blackbourn
- [Profile on Patchstack](https://patchstack.com/database/researcher/185b44a7-75e2-4c31-848d-a534cb44e821)



## Disclaimer

**This PoC is for educational purposes only.** Do not use this script to target systems without explicit permission from the system owner. Unauthorized access to systems is illegal and unethical.

## Requirements

* Python 3.x
* `requests` library

## Installation

Clone the repository and install the required Python package:

```bash
git clone https://github.com/Alucard0x1/CVE-2024-28000.git
cd CVE-2024-28000
pip install -r requirements.txt
```

## How to Use

### 1. Set Up the Target

Edit the `TARGET_SITE` and `ADMIN_USER_ID` variables in the script to point to the target WordPress site and the user ID of the Administrator you want to impersonate.

```python
# Target site and admin user ID
target_url = 'http://example.com'

admin_user_id = '1'
```

### 2. Trigger Hash Generation

The PoC first triggers the generation of the security hash on the target site using an unauthenticated AJAX request. This step is necessary if the crawler feature in the LiteSpeed Cache plugin has not been used, as the hash might not yet be generated.

### 3. Run the Brute-force Attack

Run the script to start the brute-force attack:

```bash
python litespeed_cache_poc.py
```

The script will attempt to brute-force the weak security hash by sending requests to the WordPress REST API. If a valid hash is found, it will print the successful hash value, and the exploit will be deemed successful.

### 4. Interpret the Results

* If the script prints `[SUCCESS] Valid hash found: <hash>`, it means the exploit was successful, and Administrator-level access was gained.
* If the script prints `[FAIL] Invalid hash: <hash>`, the attempt failed, and the hash was incorrect.
* If the script prints `[ERROR] Unexpected response for hash: <hash>`, it indicates that an unexpected status code was returned from the target site.




## Mitigations

To protect your WordPress site from this vulnerability, ensure that you are using the latest version of the LiteSpeed Cache plugin. Version 6.4 and above include patches that mitigate this vulnerability.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

