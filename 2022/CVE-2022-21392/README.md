# CVE-2022-21392: Local Privilege Escalation via NMR SUID in Oracle Enterprise Manager 

In Oracle installations, where the “nmr” binary is present and SUID-ed as “root”, due to insecure directory permissions, the “oracle” user can elevate his/her privileges to that of the “root” user by replacing the “nmr_macro_list” file.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://www.oracle.com/security-alerts/cpujan2022.html).

### Requirements:

This vulnerability requires:
<br/>
- Access on the local system as the "oracle" user (e.g. executing arbitrary Java code via a compromised Oracle Database)

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2022-21392/blob/main/Oracle%20Enterprise%20Manager%20-%20CVE-2022-21392.pdf).
