# CVE-2018-5353
# Zoho ManageEngine ADSelfServicePlus Client Privilege Escalation/RCE

## Information
**Vendor:** Zohocorp  
**Product:** ManageEngine ADSelfServicePlus  
**Versions Affected:** Before 5.5 build 5517  
**Researcher:** Jason Juntunen aka @missing0x00 (https://github.com/missing0x00)  
**CVSS:** 8.8  

## Description
The custom GINA/CP module in Zoho ManageEngine ADSelfService Plus before 5.5 build 5517 allows remote attackers to execute code and escalate privileges via spoofing.
It does not authenticate the intended server before opening a browser window. An unauthenticated attacker capable of conducting a spoofing attack can redirect the browser to gain execution in the context of the WinLogon.exe process. If Network Level Authentication is not enforced, the vulnerability can be exploited via RDP.
Additionally, if the web server has a misconfigured certificate then no spoofing attack is required.

### Proof of Concept
1. Conduct spoofing attack using any available method (ARP, physical access, etc.), redirecting traffic intended for the intended ADSSP server
2. Run web server on attacking host, serving binary junk file named AgentStatusUpdate.cc
3. RDP to target host (if NLA is not enforced - otherwise this attack requires physical access)
4. Click "Reset Password" link or tile on logon screen
5. Built-in client browser will be redirected to web server on attacking host, opening File Download dialog
6. Click Save, opening File Explorer dialog
7. Shift+Right-Click > "Open command window here"

[![YouTube Video CVE-2018-5353 PoC](https://img.youtube.com/vi/xrXCU6bW6Ko/0.jpg)](https://www.youtube.com/watch?v=xrXCU6bW6Ko)

![Exploit flow chart](ADSSP-PoC-Diagram.png)

### Remediation
Update the client software on all affected devices. This vulnerability was fixed in the client software included in build 5517 (April 17, 2018).

## References
**Vendor ID:** ZVE-2018-0058  
**Vendor Link:** https://www.manageengine.com/products/self-service-password/release-notes.html   
**Disclosure Link:** https://github.com/missing0x00/CVE-2018-5353  
**NIST CVE Link:** https://nvd.nist.gov/vuln/detail/CVE-2018-5353  
**CVSS Calculation:** https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator?vector=AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H  

## Disclaimer
The information contained within this advisory is supplied "as-is" with no warranties or guarantees of fitness of use or otherwise. Permission is hereby granted for the redistribution of this advisory, provided that it is not altered except by reformatting it, and that due credit is given. Permission is explicitly given for insertion in vulnerability databases and similar, provided that due credit is given to the author. The author is not responsible for any misuse of the information contained herein and accepts no responsibility for any damage caused by the use or misuse of this information. The author prohibits any malicious use of security related information or exploits by the author or elsewhere.

missingnull
