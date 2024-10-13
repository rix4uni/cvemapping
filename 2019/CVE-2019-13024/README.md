# Centreon-RCE
Centreon v.19.04 Remote Code Execution exploit (CVE-2019-13024)

Revision of https://github.com/mhaskar/CVE-2019-13024

## HOW TO USE:
1. Edit argument defaults for convenience, or don't (bottom of script)
2. If needed, edit 'edit_command' function to defeat defenses
3. '-v' for troubleshooting/verbose output (prints response content)

# EXAMPLES:
    ./centreon_rce.py whoami
    ./centreon_rce.py -t http://127.0.0.1/centreon -u MikeJones -p M1k3j0nes whoami -v
# Requirements
Requires BeautifulSoup and Requests
```bash
pip3 install requests bs4
```

# CREDIT:
https://github.com/mhaskar/ (https://github.com/mhaskar/CVE-2019-13024)

https://nvd.nist.gov/vuln/detail/CVE-2019-13024
