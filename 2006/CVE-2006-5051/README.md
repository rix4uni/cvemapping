# CVE-2024-6387
Bulk Scanning Tool for OpenSSH CVE-2024-6387 and 19 Other OpenSSH CVEs

![Banner](screens/screen1.jpg)

## Overview

Introducing a new OpenSSH bulk scanning tool! Quickly scan multiple SSH servers for security vulnerabilities like CVE-2024-6387, CVE-2006-5051, and others.  This tool is designed for scanning and reporting only - no exploitation attempts -. Enhance your security assessments today!

### Version 1.0.4

### Supported CVEs:
```sh
- CVE-2024-6387: Affects OpenSSH versions 8.5 to 9.7.
- CVE-2019-6111: Affects OpenSSH versions 5.6 to 7.9.
- CVE-2018-15473: Affects OpenSSH version 7.7.
- CVE-2016-10012: Affects OpenSSH version 6.9.
- CVE-2016-10009: Affects OpenSSH version 7.2.
- CVE-2016-6210: Affects OpenSSH version 7.2.
- CVE-2016-3115: Affects OpenSSH version 7.1.
- CVE-2016-0777: Affects OpenSSH versions 5.4 to 7.1.
- CVE-2015-6564: Affects OpenSSH version 7.0.
- CVE-2015-6563: Affects OpenSSH version 6.8.
- CVE-2015-5600: Affects OpenSSH versions 6.8 and 6.9.
- CVE-2014-2532: Affects OpenSSH version 6.6.
- CVE-2013-4548: Affects OpenSSH version 6.2.
- CVE-2012-0814: Affects OpenSSH version 6.1.
- CVE-2012-0816: Affects OpenSSH version 6.0.
- CVE-2008-5161: Affects OpenSSH version 5.0.
- CVE-2006-5051 and CVE-2008-4109: Affects OpenSSH versions before 4.4.
- CVE-2003-0190: Affects OpenSSH versions before 3.7.1p2.
- CVE-2002-0083: Affects OpenSSH versions before 3.1.
- CVE-2001-0817: Affects OpenSSH versions before 2.3.0.
```

### Install The Required Packages
```sh
pip install packaging
```

### Bulk IP Scan
```sh
python ssh.py -f targets.txt --output output.txt
```

### Sinlge IP Scan
```sh
python ssh.py -u IP
```

## Contact

For any suggestions or thoughts, please get in touch with [me](https://x.com/MohamedNab1l).


## Disclaimer

This provided tool is for educational purposes only. I do not encourage, condone, or support unauthorized access to any system or network. Use this tool responsibly and only on systems you have explicit permission to test. Any actions and consequences resulting from misuse of this tool are your own responsibility.

## References
- https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server
- https://ubuntu.com/security/CVE-2024-6387
- https://www.cve.org/CVERecord?id=CVE-2024-6387
