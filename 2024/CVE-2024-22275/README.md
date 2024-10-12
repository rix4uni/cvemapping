# CVE-2024-22275: Partial File Read in VMware vCenter Server

The vCenter Server contains a partial file read vulnerability. A malicious actor with administrative privileges on the vCenter appliance shell may exploit this issue to partially read arbitrary files containing sensitive data.

### Vendor Disclosure:

The vendor's disclosure for this vulnerability can be found [here](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/24308).

### Requirements:

This vulnerability requires:
<br/>
- Valid credentials for a user that can execute the "com.vmware.rvc" command

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2024-22275/blob/main/VMware%20vCenter%20-%20CVE-2024-22275.pdf).
