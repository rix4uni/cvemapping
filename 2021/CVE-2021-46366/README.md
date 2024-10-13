# CVE-2021-46366: Credential Bruteforce Attack via CSRF + Open Redirect in Magnolia CMS

An issue in the Login page of Magnolia CMS v6.2.3 and below allows attackers to exploit both an Open Redirect vulnerability and Cross-Site Request Forgery (CSRF) in order to brute force and exfiltrate users' credentials.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://docs.magnolia-cms.com/product-docs/6.2/Releases/Release-notes-for-Magnolia-CMS-6.2.4.html#_security_advisory).

### Requirements:

This vulnerability requires:
<br/>
- Convincing a user to access the malicious CSRF HTML page

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2021-46366/blob/main/Magnolia%20CMS%20-%20CVE-2021-46366.pdf).
