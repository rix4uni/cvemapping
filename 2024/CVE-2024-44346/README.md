![Alt Text](https://github.com/Shauryae1337/CVE-2024-44346/blob/main/%5BCVE-2024-44346%5D.jpg)


# CVE Disclosure: [CVE-2024-44346]

**Date:** [13-09-2024]

## Summary

A vulnerability was identified in Tosibox  tbsetup.exe version 4.0.0.0  , which could allow local privilege escalation . This issue has been assigned the identifier **[CVE-2024-44346]** .The vendor has released an advisory with further details and remediation steps.

## Affected Products

- **Vendor**: Tosibox 
- **Product**: tbsetup.exe
- **Version**: 4.0.0.0

## Vulnerability Description

Tosibox was informed about the issue in Tosibox Key software that could potentially allow execution of arbitrary code when running Tosibox Key installer (tbsetup.exe). A successful attempt would require the local user having downloaded or otherwise placed, a malicious binary application in the same directory as installer binary and then running the installer.

### Impact

If successful, the attackers code would execute with the elevated privileges of the application.

## Vendor Advisory

The vendor, Tosibox, has released an advisory regarding this vulnerability. You can view the advisory at the following link:

- https://tosibox.service-now.com/customer_portal?id=kb_article_view&sys_kb_id=569a9b4a3318de108efa2c023d5c7bc5

## Remediation

It is strongly recommended that users of the affected products take the following actions:

1. Update to the fixed version as mentioned in the vendor's advisory: **The new version (4.0.1) of Tosibox Key for Windows**.

## Credit

This vulnerability was discovered by Shaurya & Sahil Shah , and we thank the vendor, Tosibox, for their cooperation in releasing a patch.

## Timeline

- **Date of Discovery**: [5 August 2024]
- **Vendor Notification**: [27 Aug 2024]
- **Vendor Acknowledgment**: [13 Aug 2023]
- **Patch Release**: [27 Aug 2024]
- **Public Disclosure**: [13 Sept 2024]

## References

- [Link to CVE entry](https://www.cve.org/CVERecord?id=CVE-2024-44346)
- [Link to Vendor Advisory](https://tosibox.service-now.com/customer_portal?id=kb_article_view&sys_kb_id=569a9b4a3318de108efa2c023d5c7bc5)


## Contact

If you have any questions or need more information, feel free to reach out at [shaurya1337@gmail.com].
