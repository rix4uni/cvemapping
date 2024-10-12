## Description

This script is a PoC for CVE-2024-39304, where a SQLi is possible due to a lack of sanitization in the ChurchCRM project.

## Usage

```python3 CVE-2024-39304.py -u <USERNAME> -p <PASSWORD> -b <URL> -v```

Example: ```python3 CVE-2024-39304.py -u FirstLast -p Password123 -b http://localhost/churchcrm -v```

## Links
- https://github.com/ChurchCRM/CRM/security/advisories/GHSA-2rh6-gr3h-83j9
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-39304
