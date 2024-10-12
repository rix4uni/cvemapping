# CVE-2023-49964: FreeMarker Server-Side Template Injection in Alfresco

An issue was discovered in Hyland Alfresco Community Edition <=7.2.0. By inserting malicious content in the folder.get.html.ftl file, an attacker may perform SSTI (Server-Side Template Injection) attacks, which can leverage FreeMarker exposed objects to bypass restrictions and achieve RCE (Remote Code Execution).

<strong>Note:</strong> This issue exists because of an incomplete fix for CVE-2020-12873.

### NVD Disclosure:

The disclosure for this vulnerability can be found [here](https://nvd.nist.gov/vuln/detail/CVE-2023-49964).

### Requirements:

This vulnerability requires:
<br/>
- Valid user credentials

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2023-49964/blob/main/Alfresco%20-%20CVE-2023-49964.pdf).

### Additional Resources:

Initial [vulnerability (CVE-2020-12873)](https://nvd.nist.gov/vuln/detail/CVE-2020-12873) and [blogpost](https://securitylab.github.com/advisories/GHSL-2020-039-alfresco/) by [Alvaro "pwntester" Munoz](https://github.com/pwntester) that inspired the SSTI research and finding of this vulnerability.

[SSTI Case study: Alfresco](https://portswigger.net/research/server-side-template-injection) by PortSwigger Research

The SSTI gadget used to escape the FreeMarker sandbox was inspired from this [article](https://www.synacktiv.com/publications/exploiting-cve-2021-25770-a-server-side-template-injection-in-youtrack) by [Vincent Herbulot of Synacktiv](https://www.synacktiv.com/en/our-team/pentest)

### Timeline:

- This vulnerability was initially reported to security@alfresco.com on 22-Feb-2022
- Hyland reached out and the report was resubmitted to appsecurity@Hyland.com on 07-Apr-2022
- Retested the vulnerability on 19-Jan-2023 and noticed that the vulnerability was fixed and the vendor decided to silently patch it (no advisory, no CVE, no communication)
- Publically disclosed the vulnerability on 09-Dec-2023
