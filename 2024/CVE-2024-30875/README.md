
---

# Cross-Site Scripting (XSS) Vulnerability in `jquery-ui` v1.13.1

## Description

A Cross-Site Scripting (XSS) vulnerability has been identified in the `jquery-ui` JavaScript library, version 1.13.1. This vulnerability allows a remote attacker to obtain sensitive information and execute arbitrary code by injecting a crafted payload into the `window.addEventListener` component.

## Additional Information

The vulnerability is found in the `window.addEventListener` function and is triggered through a Reflected Cross-Site Scripting (XSS) attack. The attack vector involves injecting malicious JavaScript code that is executed when the payload is processed.

### Vulnerable Payload Example

```plaintext
%22onmouseover=%27sil9(9483)%27bad=%22&h3r90"><script>alert("Spartans-Confirm-XXS")</script>lh34l=1
```

### Proof of Concept (POC)

An example URL demonstrating this vulnerability:

```plaintext
https://example.com/catalog/product/view/id/22675/?"onmouseover='sil9(9483)'bad="&h3r90"><script>alert("XXS-Confirmed")</script>lh34l=1
```

> **Note:** This URL is provided for educational purposes and should not be used maliciously.

## Vulnerability Details

- **Vulnerability Type:** Cross-Site Scripting (XSS)
- **Vendor of Product:** JavaScript Library
- **Affected Product Code Base:** `jquery-ui` - 1.13.1
- **Affected Component:** `window.addEventListener`
- **Attack Type:** Remote

## Impact

Exploiting this vulnerability allows attackers to perform actions such as stealing cookies and session tokens, potentially leading to account takeover.

## Attack Vectors

To exploit this vulnerability, an attacker needs to lure a victim into clicking on a specially crafted link that contains the malicious payload.

## Mitigation

Users of the affected `jquery-ui` library should update to the latest version where this vulnerability has been patched. Avoid clicking on suspicious links and ensure your applications are using secure coding practices to sanitize and validate all user inputs.

## CVE Impact

Cross-site scripting can result in unauthorized actions on behalf of the user, potentially leading to the theft of sensitive information and full account compromise.

---

**Disclaimer:** This information is provided for educational and research purposes only. Unauthorized use of this information for malicious purposes is prohibited and may be punishable under applicable laws.
