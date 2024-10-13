# CVE-2021-42562: Improper Access Control in MITRE Caldera

Caldera (versions <=2.8.1) does not properly segregate user privileges, resulting in non-admin users having access to read and modify configuration or other components which should only be accessible by admin users. 

### Vendor Disclosure:

The vendor's disclosure for this vulnerability can be found [here](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42562).

### Requirements:

This vulnerability requires:
<br/>
- Valid non-admin user credentials

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2021-42562/blob/main/Caldera%20-%20CVE-2021-42562.pdf).

### Additional Resources:

This vulnerability allows a non-admin user to exploit the vulnerability [CVE-2021-42559: Command Injection via Configurations in MITRE Caldera](https://github.com/mbadanoiu/CVE-2021-42559) in order to achieve remote code execution.
