# Description

This script is a Proof of Concept (PoC) exploit I developed for [CVE-2023-24078](https://nvd.nist.gov/vuln/detail/CVE-2023-24078). After trying the publicly available PoCs that were not functional and facing frustration in trying to troubleshoot them, I just created my own script.

# Usage
```
usage: python3 CVE-2023-24078.py [-h] -lh LHOST -lp LPORT -th RHOST -tp RPORT 

A PoC script for exploiting CVE-2023-24078.

Required arguments:
  -lh LHOST, --lhost LHOST      Listening Host
  -lp LPORT, --lport LPORT      Listening Port
  -th RHOST, --rhost RHOST      Target Host IP
  -tp RPORT, --rport RPORT      Port of the target 

```
<img src="/exploit.png" width="1200px">
