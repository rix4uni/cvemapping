# CVE-2020-13965: Cross-Site Scripting via Malicious XML Attachment in Roundcube Webmail

A Cross-Site scripting (XSS) vulnerability exists in Roundcube versions before 1.4.5 and 1.3.12.

By leveraging the parsing of "text/xml" attachment, an attacker can bypass the Roundcube script filter and execute arbitrary malicious JavaScript in the victim's browser when the malicious attachment is clicked/previewed.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://roundcube.net/news/2020/06/02/security-updates-1.4.5-and-1.3.12).

### Requirements:

This vulnerability requires:
<br/>
- Waiting for a Roundcube user to open the attachment containg the XSS

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2020-13965/blob/main/Roundcube%20Disclosures%20-%20CVE-2020-13965.pdf).

