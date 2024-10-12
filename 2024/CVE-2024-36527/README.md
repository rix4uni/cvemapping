# CVE-2024-36527 PoC and Bulk Scanner
![Banner](screens/screen.jpg)

## Overview

POC for CVE-2024-36527: puppeteer-renderer v.3.2.0 and before is vulnerable to Directory Traversal. Attackers can exploit the URL parameter using the file protocol to read sensitive information from the server.

Based on the security advisory published by [Zac Wang](https://gist.github.com/7a6163/25fef08f75eed219c8ca21e332d6e911) , POC was created by [M Ali](https://x.com/MohamedNab1l).

## How to Use

### Single Target Scan

To scan a single target endpoint:
```sh
python cve-2024-36527.py -u target
```

### Bulk Target Scan
To mass scan bulk targets:
```sh
python cve-2024-36527.py -f targets.txt
```

## Installation

### Minimum Requirements

- Python 3.6 or higher
- `requests` library

### Installing The Script

```sh
git clone https://github.com/bigb0x/cve-2024-36527.git; cd cve-2024-36527
```

### Installing Required Packages

Install the required packages using pip:

```sh
pip install requests
```

## Disclaimer

I'm not a professional developer; I code as a hobby. I like to create my own tools for fun and educational purposes only. I 'm releasing this tool is for educational use only. I do not support or encourage hacking or unauthorized access to any system or network. Please use this tool responsibly and only on systems where you have clear permission to test. You are responsible for any misuse.

## References

- https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2024-36527
- https://github.com/zenato/puppeteer-renderer/issues/97
- https://gist.github.com/7a6163/25fef08f75eed219c8ca21e332d6e911
