# CVE-2023-20048 — Cisco RV Series PoC & Exploit

**⚠ WARNING:** For **authorized testing only**. Do not use against systems you do not own or have written permission to test. This is a **Proof of Concept** for **authorized testing only**.  

## What this is
Small repository with:
- `CiscoPoc.py` — harmless PoC to check for CVE-2023-20048.
- `CiscoRCE.py` — exploit that attempts a reverse shell via the vulnerable `form2ping.cgi`.
- 
## **Description**  
This script checks if a **Cisco RV Series router** is vulnerable to **CVE-2023-20048**, a command injection flaw leading to **RCE as root**.  

## Requirements
- Python 3.8+
- `requests` (`pip install requests`)

## References

- CVE record: [CVE-2023-20048 — NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-20048).  
- Cisco advisory: [Cisco Security Advisory — CVE-2023-20048](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-fmc-cmd-inj-29MP49hN).  

> ⚠ Note: According to the official NVD and Cisco advisory, CVE-2023-20048 is associated with Cisco Firepower Management Center (FMC). Make sure this CVE actually applies to the Cisco RV Series devices you are testing — if not, correct the CVE/advisory links to the appropriate CVE.  

### Check (PoC)
```bash
python3 CiscoPoc.py -t <TARGET_IP> -u <USER> -p <PASS>
