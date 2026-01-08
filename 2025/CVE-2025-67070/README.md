Intelbras NVD 9032 R Ftd – Critical Password Reset Vulnerability

Discovered by: Theo Cia

CVE: CVE-2025-67070
Status: Reported to vendor
Date Discovered: November 2025
Impact: Full administrative access via MFA bypass
Firmware: V2.800.00IB00C.0.T
Build Date: 2022-08-17


🛡️ Summary

A critical vulnerability in the Intelbras NVD 9032 R Ftd IP CFTV device allows an attacker to bypass the multi-factor authentication during password recovery. This results in the ability to change the admin password and gain full access to the administrative panel.

⚠️ Vulnerability Details

Affected component: Password recovery endpoint

Vulnerability class: Improper Access Control (CWE-284)

Attack vector: Web-based response manipulation (interception/proxy)


Impact

This vulnerability allows unauthenticated attackers to:

Reset the admin password

Bypass multi-factor authentication

Gain full administrative access to the NVR panel

🔒 Mitigation

No official fix is available as of the publication date. Intelbras has been notified.

📩 Contact

For more information or coordination, please contact:
theo.cia@guardsi.com.br
