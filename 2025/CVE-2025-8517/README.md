# Session Fixation in Vvveb CMS v1.0.6.1

- **Author:** Andrew Paul
    
- **Date of Discovery:** June 9th, 2025
    
- **Vendor:** Vvveb
    
- **Vendor URL:** [http://vvveb.com](http://vvveb.com)
    
- **Vendor GitHub:** [https://github.com/givanz/Vvveb](https://github.com/givanz/Vvveb)
    
- **Affected Version:** 1.0.6.1 (and likely prior versions)
- **CVE ID:** [CVE-2025-8517](https://nvd.nist.gov/vuln/detail/CVE-2025-8517)

## Summary

A Session Fixation vulnerability, classified as [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html), was discovered in the authentication mechanism of Vvveb CMS version 1.0.6.1. The system fails to create and enforce a new session identifier upon successful login. This fundamental flaw allows for two attack variations: a standard Session Fixation attack using a server-issued session ID, and a more severe attack where an attacker can invent an arbitrary string to be used as the session ID. In both cases, the vulnerability can be exploited to hijack a user's authenticated session, leading to a full account takeover.

## OWASP Top 10 2021 Mapping

This vulnerability maps to several categories in the [OWASP Top 10 2021:](https://owasp.org/Top10)

- [**A01:2021 - Broken Access Control:**](https://owasp.org/Top10/A01_2021-Broken_Access_Control) The ultimate impact of the attack is a complete failure of access control, as the attacker gains all the permissions and access rights of the hijacked user account.
  
- [**A04:2021 - Insecure Design:**](https://owasp.org/Top10/A04_2021-Insecure_Design) The authentication process is insecure by design because it lacks a fundamental security control: the regeneration of session tokens upon a change in privilege level.

- [**A07:2021 - Identification and Authentication Failures:**](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures) The application fails to properly manage the lifecycle of session identifiers after login, allowing an attacker to fixate a session and impersonate a user.

## Vulnerability Details

The root cause of this vulnerability is a complete failure to manage session state securely during the authentication process. This manifests in two distinct but related flaws:

1. **Failure to Regenerate Legitimate Session IDs:** The application does not generate a new `PHPSESSID` after a valid login. This allows an attacker to visit the login page, obtain a legitimate pre-authentication session ID, fixate it within a victim's browser, and later use that same ID to hijack the session.
    
2. **Acceptance of Arbitrary Session IDs:** More critically, the application's session mechanism blindly trusts client-provided identifiers. An attacker does not need a real session ID from the server; they can invent any arbitrary string (e.g., 'hacked'), which the server will accept and then elevate to an authenticated session upon login. This removes a step for the attacker and highlights the profound nature of the flaw.
    

## Potential Attack Vectors

This vulnerability can be exploited through any vector that allows an attacker to set or "fix" a cookie in the victim's browser. Common vectors include:

- **Cross-Site Scripting (XSS):** A separate XSS flaw could allow for remote exploitation.
    
- **Physical Access (Shared Workstation):** An attacker can manually set the cookie on a shared computer.
    
- **Man-in-the-Middle (MitM):** An attacker on an insecure network could intercept traffic to plant the cookie.
    

## Proof of Concept (PoC)

This PoC demonstrates a full account takeover of an administrator account from a separate machine, highlighting the most severe attack path using an attacker-invented identifier.

**Steps:**

1. **Attacker Invents an Identifier:** The attacker chooses an arbitrary string to act as the session identifier, for example: `session-hijacked-by-andy`.
    
2. **Attacker Plants the Cookie:** On a victim's machine, the attacker uses the browser's developer tools to set the `PHPSESSID` cookie to `session-hijacked-by-andy` for the Vvveb CMS domain.
    
3. **Victim (Administrator) Logs In:** The victim, using the same browser, logs into the Vvveb CMS with their administrator credentials.
    
4. **System Failure:** The CMS validates the victim's credentials but fails to generate a new session cookie. Instead, it promotes the attacker's cookie (`session-hijacked-by-andy`) to a fully authenticated administrator session.
    
5. **Attacker Hijacks Session:** From a separate computer, the attacker sets their browser's `PHPSESSID` cookie to `session-hijacked-by-andy` and navigates to the Vvveb CMS admin dashboard.
    

**Result:** The attacker is granted immediate and complete administrative access to the CMS without needing the victim's password.

## Impact

A successful exploit results in a complete compromise of the targeted user's account. If the victim is an administrator, the impact is critical and includes:

- **Complete Administrative Control:** The attacker gains full control over the CMS, equivalent to the hijacked administrator.
    
- **Data Compromise:** Full ability to read, modify, export, or delete all site content, user data, and sensitive configuration details.
    
- **System Persistence:** The attacker can create a new user with full administrator privileges. This provides them with a persistent backdoor into the system, even after the original hijacked session expires or the legitimate administrator logs out.
    
- **Further Attacks:** The compromised administrator account can be used to upload malicious files (e.g., web shells) or launch further attacks against the underlying server and its visitors.
    

## Recommended Mitigation

The application must regenerate the session identifier upon any change in privilege level, especially user authentication. The standard implementation in PHP is to call `session_regenerate_id(true);` immediately after validating a user's credentials and before granting access to the authenticated part of the application.

## Disclosure Timeline

- **Discovery Date:** June 9th, 2025
    
- **Vendor Notification Date:** June 10th, 2025
    
- **Vendor Acknowledgment Date:** June 16th, 2025
    
- **Patch Release Date:** [June 17th, 2025](https://github.com/givanz/Vvveb/releases/tag/1.0.7)
    
- **Public Disclosure Date:** July 26th, 2025
