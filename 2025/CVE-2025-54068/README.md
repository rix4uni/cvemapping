# Livewire2025CVE
# Livewire CVE-2025-54068 Scanner

Automated vulnerability scanner for detecting CVE-2025-54068 in Laravel applications using Livewire v3.0.0-beta.1 through v3.6.3.

## Overview
This tool scans a list of websites for indicators of the critical Livewire remote code execution vulnerability (CVE-2025-54068, CVSS 9.2). Vulnerable sites are separated into `vuln.txt` while safe sites are saved to `safe.txt`.

**Coded by z0d131482700x Persephrak CyberSecurity Team**

## Features
- Multi-threaded scanning for performance
- Detects Livewire JavaScript files and version patterns
- Identifies `wire:` component attributes
- Graceful error handling and timeouts
- Generates categorized output files with headers

## Requirements
- Python 3.6+
- `requests` library (`pip install requests`)


## Detection Method
The scanner checks for:
- Livewire endpoints: `/livewire/livewire.js`, `/livewire/message`
- Version patterns: `v3.[0-6].[0-3]` in JavaScript files
- HTML fingerprints: `wire:` attributes and Livewire references
- HTTP status codes and response content analysis

## Limitations
- **Indicator-based detection only**: Does not attempt active exploitation
- **False positives possible**: Manual verification recommended for `vuln.txt` sites
- **Version detection limitations**: Relies on exposed JavaScript files
- **Network-only**: Cannot detect server-side configurations

## Security Recommendations
For sites in `vuln.txt`:
1. Upgrade Livewire to v3.6.4 or higher immediately
2. Audit all Livewire components for property hydration usage
3. Implement Web Application Firewall (WAF) rules
4. Monitor server logs for suspicious Livewire requests
5. Conduct full penetration testing

## Roadmap
- Active vulnerability confirmation (non-destructive)
- Custom detection signatures
- Database of known vulnerable applications
- Reporting dashboard
- CI/CD integration


## Support
Report issues via GitHub Issues. For security vulnerabilities, please contact the Persephrak CyberSecurity Team directly.

## Disclaimer
This tool is provided for security research and defensive purposes only. The authors are not responsible for misuse or any damages resulting from its use. Always obtain proper authorization before scanning websites.
