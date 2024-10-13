# Fix-WinVerifyTrustSignatureValidationVuln
Fix WinVerifyTrust Signature Validation Vulnerability, CVE-2013-3900[^1], QID-378332[^2]

_**This Fix is intended for 64-bit Windows Computers**_

This PowerShell code is one way to fix the vulnerability - aside from creating a .reg file and using ```reg import <file.reg>``` to import the new registry key.

Full Packaged Script:<br>
If HKLM:\Software\Microsoft\Cryptography\Wintrust\Config not found, create path and key.<br>
If key is found, then show results of key - do nothing. etc.<br>

The new registry key is expected to be of type: **REG_SZ**

---
# _The following is quoted from MSRC_ ->

"**Does the new verification behavior affect already-installed software?**

The new stricter verification behavior, when enabled, applies primarily to portable executable (PE) binaries that are signed with the Windows Authenticode signature format. Binaries that are not signed with this format or that do not use WinVerifyTrust to verify signatures are not affected by the new behavior. Binaries most likely to be affected are PE installer files distributed via the Internet that are customized at time of download. The most common scenario in which users could perceive an impact is during the downloading and installation of new applications. This is the case only if customers have chosen to enable the stricter verification behavior, after which users may observe warning messages when attempting to install new applications with signatures that fail validation.

**Why is Microsoft republishing a CVE from 2013?**

We are republishing CVE-2013-3900 in the Security Update Guide to update the Security Updates table and to inform customers that the EnableCertPaddingCheck is available in all currently supported versions of Windows 10 and Windows 11. While the format is different from the original CVE published in 2013, the information herein remains unchanged from the original text published on December 10, 2013.

Microsoft does not plan to enforce the stricter verification behavior as a default functionality on supported releases of Microsoft Windows. This behavior remains available as an opt-in feature via reg key setting, and is available on supported editions of Windows released since December 10, 2013. This includes all currently supported versions of Windows 10 and Windows 11. The supporting code for this reg key was incorporated at the time of release for Windows 10 and Windows 11, so no security update is required; however, the reg key must be set. See the Security Updates table for the list of affected software.

**Vulnerability Description**

A remote code execution vulnerability exists in the way that the WinVerifyTrust function handles Windows Authenticode signature verification for portable executable (PE) files. An anonymous attacker could exploit the vulnerability by modifying an existing signed executable file to leverage unverified portions of the file in such a way as to add malicious code to the file without invalidating the signature. An attacker who successfully exploited this vulnerability could take complete control of an affected system. An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights.

If a user is logged on with administrative user rights, an attacker who successfully exploited this vulnerability could take complete control of an affected system. An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights. Users whose accounts are configured to have fewer user rights on the system could be less impacted than users who operate with administrative user rights.

Exploitation of this vulnerability requires that a user or application run or install a specially crafted, signed PE file. An attacker could modify an existing signed file to include malicious code without invalidating the signature. This code would execute in the context of the privilege in which the signed PE file was launched.

In an email attack scenario, an attacker could exploit this vulnerability by sending a user an email message containing the specially crafted PE file and convincing the user to open the file.

In a web-based attack scenario, an attacker would have to host a website that contains a specially crafted PE file. In addition, compromised websites and websites that accept or host user-provided content could contain specially crafted content that could be used to exploit this vulnerability. An attacker would have no way to force users to visit a website that is hosting the specially crafted PE file. Instead, an attacker would have to convince users to visit the website, typically by getting them to click a link in an email message or Instant Messenger message that directs them to the attacker's website.

**Update History**

On December 10, 2013, Microsoft released an update for all supported releases of Microsoft Windows that changes how signatures are verified for binaries signed with the Windows Authenticode signature format. This change can be enabled on an opt-in basis. When enabled, the new behavior for Windows Authenticode signature verification will no longer allow extraneous information in the WIN_CERTIFICATE structure, and Windows will no longer recognize non-compliant binaries as signed. On July 29, 2014 Microsoft announced that it no longer plans to enforce the stricter verification behavior as a default functionality on supported releases of Microsoft Windows. To this date, it remains available as an opt-in feature in all currently supported releases of Microsoft Windows.

**Recommendation.** Microsoft recommends that executables authors consider conforming all signed binaries to the new verification standard by ensuring that they contain no extraneous information in the WIN_CERTIFICATE structure. Microsoft also recommends that customers appropriately test this change to evaluate how it will behave in their environments..."[^1]

[^1]: MSRC.Microsoft - WinVerifyTrust Signature Validation Vulnerability
  https://msrc.microsoft.com/update-guide/vulnerability/CVE-2013-3900

[^2]: Recent changes in Qualys Coverage for Microsoft WinVerifyTrust Signature Validation Vulnerability (CVE-2013-3900)
  https://notifications.qualys.com/product/2023/04/07/recent-changes-in-qualys-coverage-for-microsoft-winverifytrust-signature-validation-vulnerability-cve-2013-3900

