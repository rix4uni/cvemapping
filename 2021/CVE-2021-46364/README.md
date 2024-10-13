# CVE-2021-46364: YAML Deserialization in Magnolia CMS

Magnolia (versions <=6.2.3) has a Snake YAML parser which is vulnerable to deserialization attacks that can allow an attacker to call arbitrary Java constructors when importing YAML files. <br/>
Remote Code Execution has been achieved using this vulnerability.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://docs.magnolia-cms.com/product-docs/6.2/Releases/Release-notes-for-Magnolia-CMS-6.2.4.html#_security_advisory).

### Requirements:

This vulnerability requires:
<br/>
- Valid user credentials

### Proof Of Concept:
More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2021-46364/blob/main/Magnolia%20CMS%20-%20CVE-2021-46364.pdf).
