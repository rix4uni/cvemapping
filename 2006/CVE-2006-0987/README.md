## DNS Amplification DDoS Detection and Verification Tool

This script is designed to identify and verify potential DNS servers vulnerable to exploitation in DNS amplification distributed denial-of-service (DDoS) attacks. It addresses the limitations of automated vulnerability scanners like Nessus, which may generate [false positives](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/ "false positives") when detecting this issue using plugin 35450.

### Background

DNS amplification attacks are a type of reflection-based DDoS attack that exploits misconfigured or open DNS resolvers. Attackers send small DNS queries with spoofed source IP addresses, causing the DNS server to send large responses to the victim's IP address. This amplifies the attack traffic, potentially overwhelming the target's network resources.

### Functionality

The script performs the following key functions:

1. Bulk domain processing: Analyzes multiple domains efficiently to identify potential vulnerabilities.
2. DNS query simulation: Sends specially crafted DNS queries to test for amplification behavior.
3. Response analysis: Examines DNS responses to determine if the server exhibits characteristics conducive to amplification attacks.
4. False positive reduction: Implements additional checks to minimize false positives compared to basic vulnerability scans.

### Use Case

This tool is particularly useful for:

- Security professionals conducting large-scale DNS infrastructure audits
- Network administrators verifying the security posture of their DNS servers
- Researchers studying DNS amplification attack vectors

By providing a more accurate assessment of DNS amplification vulnerabilities, this script enables organizations to prioritize mitigation efforts and enhance their DDoS resilience.

------------


# Usage
## Clone the repository
```bash
git clone https://github.com/pcastagnaro/dns_amplification_scanner/
cd dns_amplification_scanner
```

## Create a Virtual Environment
```bash
python3 -m venv myenv; source myenv/bin/activate
```

## Install Dependancies
```bash
pip install colorama
```

## Run the Script
```bash
python dns_amplification_scanner.py <DNS> --domains <DOMAIN_LIST> --type ANY 
```

## Example
```bash
python dns_amplification_scanner.py 8.8.8.8 --domains domains.txt --type ANY 
```

![Amplification](https://github.com/user-attachments/assets/9ca0079f-214b-40ac-b82c-639de79d0566)
