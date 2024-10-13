# CVE-2021-46363: Formula Injection in Magnolia CMS

An issue in the Export function of Magnolia v6.2.3 and below allows attackers to perform Formula Injection attacks via crafted CSV/XLS files. These formulas may result in arbitrary code execution on a victim's computer when opening the exported files with Microsoft Excel.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://docs.magnolia-cms.com/product-docs/6.2/Releases/Release-notes-for-Magnolia-CMS-6.2.4.html#_security_advisory).

### Requirements:

This vulnerability requires:
<br/>
- Valid user credentials

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2021-46363/blob/main/Magnolia%20CMS%20-%20CVE-2021-46363.pdf).
