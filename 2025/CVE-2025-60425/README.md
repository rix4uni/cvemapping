## Session Persistence After Enabling 2FA

## Overview
The Nagios Fusion application (version 2024R1.2 and 2024R2) contains a high security flaw where existing sessions remain valid even after enabling Two-Factor Authentication (2FA). Specifically, when 2FA is enabled for an administrator account, the application fails to invalidate all active sessions established prior to enabling 2FA. This allows an attacker or unauthorized user with access to an older session to bypass the 2FA mechanism and perform unauthorized actions.

The following issues were observed:
> Session Persistence: Sessions created before enabling 2FA remain valid without requiring the additional authentication factor.

> Unauthorized Privilege Escalation: Using these old sessions, attackers can modify crucial account details or perform administrative actions without 2FA validation.

This vulnerability arises due to a lack of session invalidation during the 2FA enablement process, resulting in the application failing to enforce the additional security mechanism for older sessions.

## Severity
- **Severity**: High
- **CWE**: CWE-613 (primary); CWE-287 (secondary)
- **CVSS Score (v3.0)**: 7.3 High
- **CVSS Vector**: AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N

## Affected Components
- **Authentication Gateway / Session Service**: Session issuance, validation, and revocation logic.
- **2FA Enrollment & Policy Engine**: Logic that upgrades an account’s assurance level without revoking existing tokens.
- **Web Frontend / API**: Authorization checks that trust legacy session state.
- **Device Management**: Remembered devices / trusted sessions store (cookies, refresh tokens, server-side sessions).

## Affected Vendor/Product
- **Product Name**- Nagios Fusion
- **Affected Version**: 2024R1.2 and 2024R2
- **Fixed Version**: 2024R2.1

## Summary of the Issue
**What happens:**
1. User enables 2FA on their account (TOTP/SMS/push/webauthn).
2. Server updates the user’s MFA/assurance state but does not invalidate or re-challenge existing sessions.
3. Any active sessions (including those on attacker-controlled clients) continue operating with the pre-2FA context, effectively bypassing the intended control uplift.

**Security Posture Gap**: Enabling 2FA is a security boundary change. Failing to force session upgrade (re-auth + 2FA) and revoke legacy sessions negates the control’s risk reduction.

**Realistic Abuse Scenarios**:
- Attacker with stolen session cookie retains access post-2FA enablement and can exfiltrate data or change account settings.
- Shared kiosk or unmanaged device keeps a live session that bypasses the new MFA requirement.

## Mitigation Recommendations
- On 2FA enrollment or factor reset, revoke all existing sessions (access + refresh tokens) across devices and require fresh primary auth + 2FA.
- Rotate session secrets (e.g., change signing keys or bump server-side session version) to invalidate stale tokens.
- Set maxAge and idleTimeout to reasonable values; reduce long-lived sessions.

## Disclosure Timeline
- **[04-01-2025]**: Vulnerability discovered  
- **[04-01-2025]**: Reported to vendor  
- **[10-01-2025]**: Vendor verified the vulnerability
- **[23-07-2025]**: Vendor patched the vulnerability with a new release
- **[16-08-2025]**: Apply For CVE
- **[23-10-2025]**: Assign CVE 

---
📌 *This repository is intended solely for vulnerability reporting and CVE reference.*
