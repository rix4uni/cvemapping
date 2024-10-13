# CVE-2021-42560: Unsafe XML Parsing in MITRE Caldera

The Debrief plugin in Caldera (versions <=2.9.0) receives base64 encoded "SVG" parameters when generating a PDF. These SVG are parsed in an unsafe manner and can be leveraged for XXE attacks (e.g. File Exfiltration, Server-Side Request Forgery, Out of Band Exfiltration, etc.). 

### Vendor Disclosure:

The vendor's disclosure for this vulnerability can be found [here](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42560).

### Requirements:

This vulnerability requires:
<br/>
- Valid user credentials

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2021-42560/blob/main/Caldera%20-%20CVE-2021-42560.pdf).
