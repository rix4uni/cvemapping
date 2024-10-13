# CVE-2019-1332: Reflected Cross-Site Scripting in Microsoft SQL Server Reporting Services

A cross-site scripting (XSS) vulnerability exists when Microsoft SQL Server Reporting Services (SSRS) does not properly sanitize a specially-crafted web request to an affected SSRS server. An attacker who successfully exploited the vulnerability could run scripts in the context of the targeted user. The attacks could allow the attacker to read content that the attacker is not authorized to read, execute malicious code, and use the victim's identity to take actions on the site on behalf of the user, such as change permissions and delete content.

<strong>Note:</strong> To exploit the vulnerability, an attacker would need to convince an authenticated user to click a specially-crafted link to an affected SSRS server.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://msrc.microsoft.com/update-guide/en-us/advisory/CVE-2019-1332).

### Requirements:

This vulnerability requires:
<br/>
- Convincing an authenticated SSRS user to click on a specially-crafted link

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2019-1332/blob/main/Microsoft%20SQL%20Server%20Reporting%20Services%20-%20CVE-2019-1332.pdf).
