# CVE-2018-5354
# ANIXIS Password Reset Client Privilege Escalation/RCE

## Information
**Vendor:** ANIXIS  
**Product:** ANIXIS Password Reset Client  
**Versions Affected:** Before version 3.22  
**Researcher:** Jason Juntunen aka @missing0x00 (https://github.com/missing0x00)  
**CVSS:** 8.8

## Description
The custom GINA/CP module in ANIXIS Password Reset Client before version 3.22 allows remote attackers to execute code and escalate privileges via spoofing.
When the client is configured to use HTTP, it does not authenticate the intended server before opening a browser window. An unauthenticated attacker capable of conducting a spoofing attack can redirect the browser to gain execution in the context of the WinLogon.exe process. If Network Level Authentication is not enforced, the vulnerability can be exploited via RDP.

### Proof of Concept
1. Conduct spoofing attack using any available method (ARP, physical access, etc.), redirecting traffic intended for the intended password reset server
2. Run web server on attacking host, serving binary junk file named pwreset
3. RDP to target host (if NLA is not enforced - otherwise this attack requires physical access)
4. Click "Reset Password" link or tile on logon screen
5. Built-in client browser will be redirected to web server on attacking host, opening File Download dialog
6. Click Save, opening File Explorer dialog
7. Shift+Right-Click > "Open command window here"

### Remediation
Update the client software on all affected devices. This vulnerability was fixed in the client version 3.22 (January 29, 2018). Additionally, ensure that the server and client are configured to use HTTPS with a valid certificate.

## References
**Vendor ID:** APRSA005  
**Vendor Link:** https://anixis.com/products/apr/default.htm  
**Disclosure Link:** https://github.com/missing0x00/CVE-2018-5354   
**NIST CVE Link:** https://nvd.nist.gov/vuln/detail/CVE-2018-5354   
**CVSS Calculator:** https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator?vector=AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

## Disclaimer
The information contained within this advisory is supplied "as-is" with no warranties or guarantees of fitness of use or otherwise. Permission is hereby granted for the redistribution of this advisory, provided that it is not altered except by reformatting it, and that due credit is given. Permission is explicitly given for insertion in vulnerability databases and similar, provided that due credit is given to the author. The author is not responsible for any misuse of the information contained herein and accepts no responsibility for any damage caused by the use or misuse of this information. The author prohibits any malicious use of security related information or exploits by the author or elsewhere.

missingnull
