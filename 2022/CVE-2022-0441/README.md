![image](https://github.com/tegal1337/CVE-2022-0441/assets/31664438/9982fb7c-5248-4e30-9bd7-59a5c78635af)



A vulnerability classified as critical was found in MasterStudy LMS Plugin up to 2.7.5 on WordPress (WordPress Plugin). This vulnerability affects an unknown part of the component New Account Handler. The manipulation with an unknown input leads to a privileges management vulnerability. The CWE definition for the vulnerability is CWE-269. The software does not properly assign, modify, track, or check privileges for an actor, creating an unintended sphere of control for that actor. As an impact it is known to affect confidentiality, integrity, and availability.

The weakness was disclosed 03/07/2022 as 2667195. The advisory is available at wpscan.com. This vulnerability was named CVE-2022-0441 since 02/01/2022. The technical details are unknown and an exploit is not available. This vulnerability is assigned to T1068 by the MITRE ATT&CK project.

Upgrading to version 2.7.6 eliminates this vulnerability. Applying a patch is able to eliminate this problem. The bugfix is ready for download at plugins.trac.wordpress.org. The best possible mitigation is suggested to be upgrading to the latest version.

# Usage 

```bash
git clona https://github.com/tegal1337/CVE-2022-0441
cd CVE-2022-0441
npm install
node index.js https://targeturl.com
```

# Refference

https://vuldb.com/?id.194302

https://nvd.nist.gov/vuln/detail/cve-2022-0441

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0441

