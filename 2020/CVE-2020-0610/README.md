# CVE-2020-0610 BlueGate Lab - Windows RD Gateway UDP/DTLS RCE

[![CVE-2020-0610](https://img.shields.io/badge/CVE--2020--0610-Critical-red)](https://nvd.nist.gov/vuln/detail/CVE-2020-0610)
[![BlueGate](https://img.shields.io/badge/BlueGate-PoC-orange)](https://gitlab.com/ind3p3nd3nt/BlueGate)
[![Nuclei Template](https://img.shields.io/badge/Nuclei-Template-blue)](https://github.com/projectdiscovery/nuclei-templates)

A comprehensive reproducible laboratory environment for **CVE-2020-0610** (BlueGate), a critical pre-authentication remote code execution vulnerability in Microsoft Windows Remote Desktop Gateway (RD Gateway). This lab enables security researchers to safely test and validate the vulnerability using minimal, non-destructive DTLS handshake techniques.

## 🎯 Vulnerability Overview

**CVE-2020-0610** is a critical RCE vulnerability in Windows RD Gateway that allows unauthenticated attackers to execute arbitrary code by sending specially crafted UDP packets to port 3391. The vulnerability affects:

- Windows Server 2012 / 2012 R2
- Windows Server 2016
- Windows Server 2019
- Any system with RD Gateway role and UDP transport enabled

**CVSS Score:** 9.8 (Critical)
**Attack Vector:** Network (UDP/3391)
**Authentication:** None required
**Impact:** Complete system compromise

## 🔬 Lab Scope & Safety

- **Pre-authentication** DTLS handshake on UDP 3391
- Single tiny fragment transmission (BlueGate "check" method)
- **Non-destructive** - no DoS flooding or system damage
- Isolated lab environment recommended
- Compatible with Nuclei security scanner templates

## 📋 Requirements

### Infrastructure

- **Hypervisor:** Hyper-V / VMware Workstation / VirtualBox
- **Target OS:** Windows Server (2012/2012 R2/2016/2019) - unpatched
- **Network:** Isolated lab network
- **Resources:** 2GB RAM minimum, 40GB disk space

### Tools

- PowerShell (Admin privileges required)
- [Nuclei Scanner](https://github.com/projectdiscovery/nuclei) v3.4.10+
- Network connectivity testing tools (optional)

## 🚀 Quick Setup Guide

### 1. Install RD Gateway Role

```powershell
# Via Server Manager GUI
Server Manager → Add Roles and Features → Remote Desktop Services → RD Gateway
```

### 2. Enable UDP Transport

```powershell
# Via RD Gateway Manager
RD Gateway Manager → <ServerName> → Properties → Transport Settings
→ Check "Allow users to connect by using UDP" → OK
```

### 3. Configure Firewall (UDP/3391)

```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File .\scripts\add-udp-3391-firewall.ps1
```

### 4. System Validation

```powershell
# Verify RD Gateway and firewall configuration
powershell -ExecutionPolicy Bypass -File .\scripts\sanity-check.ps1
```

### 5. Vulnerability Testing

```bash
# Using Nuclei scanner
nuclei -t network/cves/2020/CVE-2020-0610.yaml \
       -u <target_host> \
       -var rdg_port=3391 \
       -var dtls_timeout=6 \
       -debug
```

## 🔍 Expected Results

### Vulnerable System

```
DEBUG_HEX:
NUCLEI_RESULT:VULNERABLE
```

### Patched System

```
DEBUG_HEX: 160303...ffff0080
NUCLEI_RESULT:NOT_VULNERABLE
```

The key indicator is the presence of the `ffff0080` trailer (little-endian representation of `0x8000ffff`) in patched systems.

## 📁 Repository Structure

```
lab-rdg-bluegate/
├── README.md                           # This comprehensive guide
├── scripts/
│   ├── add-udp-3391-firewall.ps1     # Firewall configuration
│   └── sanity-check.ps1               # System validation
└── samples/
    ├── nuclei-debug-vulnerable.txt    # Example vulnerable output
    └── nuclei-debug-patched.txt       # Example patched output
```

## 🛡️ Security Considerations

- **Isolation:** Always run in isolated lab environments
- **Snapshots:** Use VM snapshots for easy rollback
- **Network Segmentation:** Prevent lab network access to production
- **Responsible Disclosure:** Use only for authorized testing
- **Patch Management:** Apply security updates after testing

## 🔗 Related Resources

### Official Documentation

- [Microsoft Security Advisory](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2020-0610)
- [NVD Entry - CVE-2020-0610](https://nvd.nist.gov/vuln/detail/CVE-2020-0610)

### Research & Analysis

- [Kryptos Logic - RDP to RCE Analysis](https://www.kryptoslogic.com/blog/2020/01/rdp-to-rce-when-fragmentation-goes-wrong/)
- [BlueGate PoC Repository](https://gitlab.com/ind3p3nd3nt/BlueGate)
- [VulnCheck Database Entry](https://vulncheck.com/xdb/3a3f10478ff3)

### Security Tools

- [Nuclei Scanner](https://github.com/projectdiscovery/nuclei)
- [ProjectDiscovery Templates](https://github.com/projectdiscovery/nuclei-templates)

## 🤝 Contributing

This lab was created to support the security research community. Contributions are welcome:

- Improve setup scripts
- Add additional test cases
- Enhance documentation
- Report issues or bugs

## ⚖️ Legal Disclaimer

This laboratory environment is provided for **educational and authorized security testing purposes only**. Users are responsible for:

- Obtaining proper authorization before testing
- Complying with applicable laws and regulations
- Using the lab ethically and responsibly
- Not targeting systems without explicit permission

## 🏷️ Keywords

`CVE-2020-0610` `BlueGate` `RD Gateway` `Windows Server` `Remote Code Execution` `UDP` `DTLS` `Nuclei` `Security Research` `Vulnerability Lab` `Penetration Testing` `Red Team` `Blue Team` `Cybersecurity`
