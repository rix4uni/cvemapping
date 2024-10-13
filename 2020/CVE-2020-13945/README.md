# CVE-2020-13945 - Apache APISIX Remote Code Execution (RCE)

This repository contains a proof-of-concept (PoC) exploit for a vulnerability in Apache APISIX. The vulnerability arises when the Admin API is enabled and the access IP restriction rules are deleted, allowing the default token to access APISIX management data. This affects versions 1.2, 1.3, 1.4, and 1.5.

## Table of Contents

- [Overview](#overview)
- [Affected Versions](#affected-versions)
- [Setup](#setup)
- [Usage](#usage)
- [Mitigation](#mitigation)
- [Disclaimer](#disclaimer)

## Overview

Apache APISIX is a dynamic, real-time, high-performance API gateway. A critical security vulnerability exists in versions 1.2 to 1.5, where enabling the Admin API and deleting the Admin API access IP restriction rules permits unauthorized access using the default token.

## Affected Versions

- Apache APISIX 1.2
- Apache APISIX 1.3
- Apache APISIX 1.4
- Apache APISIX 1.5

## Setup

1. Clone the repository:
    ```bash
    git https://github.com/K3ysTr0K3R/CVE-2020-13945-EXPLOIT.git
    cd CVE-2020-13945
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure Apache APISIX is running and the Admin API is enabled.
2. Run the exploit script:
    ```bash
    python CVE-2020-13945.py -u <target>
    python CVE-2020-13945.py -f <target_file> -t 77
    ```
   Replace `<target(s)>` with the url of the target APISIX instance to exploit.

## Mitigation

To mitigate this vulnerability:

1. **Do not delete the Admin API access IP restriction rules.** Ensure they are configured correctly to restrict access to trusted IPs only.
2. **Change the default token.** Use a strong, unique token for accessing the Admin API.

For detailed information on configuring security settings, refer to the [Apache APISIX documentation](https://apisix.apache.org/docs/apisix/getting-started).

## Disclaimer

This PoC exploit is intended for educational purposes only. Use it at your own risk. Unauthorized use of this tool against systems without explicit permission is illegal and unethical. The author is not responsible for any damage caused by the use of this exploit.
