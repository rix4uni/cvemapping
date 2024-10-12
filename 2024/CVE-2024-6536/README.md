## Description

This script is a PoC for CVE-2024-6536, where a XSS is possible in the Zephyr Project Manager plugin for Wordpress. It requires authentication and privileges as a project manager administrator.

## Usage

```python3 CVE-2024-6536.py -u <USERNAME> -p <PASSWORD> -w <url>```

Example: ```python3 CVE-2024-6536.py -u user -p user -w http://localhost/wordpress```

## Links
- https://wpscan.com/vulnerability/ee40c1c6-4186-4b97-866c-fb0e76cedeb8/
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=2024-6536
