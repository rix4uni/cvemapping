# Atlassian Companion RCE Vulnerability Proof of Concept (CVE-2023-22524)

## Overview

This repository contains a proof of concept (PoC) for the recently discovered remote code execution vulnerability in Atlassian Companion for macOS, identified as CVE-2023-22524. This critical issue allows attackers to bypass the app's blocklist and macOS Gatekeeper, leading to potential execution of harmful code.

## Details

The vulnerability stems from an oversight in the application's handling of certain file types and its interaction with macOS security features. For a detailed analysis of the vulnerability, including the discovery process and technical specifics, please refer to our comprehensive blog post on the [Imperva Threat Research Blog](https://www.imperva.com/blog/?category=labs)

## Steps to Reproduce

1. Atlassian Companion < 2.0.0 is required.
2. Clone this repository, navigate to the `PoC` directory, and run `node server.js`.
3. Visit `http://localhost:8080/example.html` in your browser and follow the instructions.

## Additional Information

- [Imperva Threat Research Blog](https://www.imperva.com/blog/cve-2023-22524-rce-vulnerability-in-atlassian-companion-for-macos/)
- [Atlassian's Security Advisory](https://confluence.atlassian.com/security/cve-2023-22524-rce-vulnerability-in-atlassian-companion-app-for-macos-1319249492.html)

## Disclaimer

The information provided here is for educational and research purposes only. The authors are not responsible for any misuse of this information.
