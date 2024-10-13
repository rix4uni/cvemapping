# CVE-2020-12640: Local PHP File Inclusion via "Plugin Value" in Roundcube Webmail

A Path Traversal vulnerability exists in Roundcube versions before 1.4.4, 1.3.11 and 1.2.10.

Because the "\_plugins\_<PLUGIN_NAME>" parameters do not perform sanitization/input filtering, an attacker with access to the Roundcube Installer can leverage a path traversal vulnerability to include arbitrary PHP files on the local system.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://roundcube.net/news/2020/04/29/security-updates-1.4.4-1.3.11-and-1.2.10).

### Requirements:

This vulnerability requires:
<br/>
- Access to the Roundcube Webmail installer component
- Write access to the target's filesystem

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2020-12640/blob/main/Roundcube%20Disclosures%20-%20CVE-2020-12640.pdf).
