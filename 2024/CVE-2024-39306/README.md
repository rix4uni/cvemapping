## Description

This script is a PoC for CVE-2024-39306, where a RCE is possible due to a SQLi where an authenticated user can execute arbitrary commands on a server running ChurchCRM <= 5.8.0

## Usage

```python3 CVE-2024-39306.py -u <USERNAME> -p <PASSWORD> -b <URL> -c <COMMAND>```

Example: ```python3 CVE-2024-39306.py -u FirstLast -p Password123 -b http://localhost/churchcrm -c whoami```

## Links

- https://github.com/ChurchCRM/CRM/security/advisories/GHSA-r2gf-5m64-8v39
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-39306
