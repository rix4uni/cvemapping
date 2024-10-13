## CVE-2014-4936: Malwarebytes Anti-Malware and Anti-Exploit upgrade hijacking ##
=============

This repository contains the POC for CVE-2014-4936. A full writeup on how the vulnerability works and how to exploit it using the POC has been published here:
(http://blog.0x3a.com/post/104954032239/cve-2014-4936-malwarebytes-anti-malware-and)

### Timeline: ###

- Malwarebytes Anti-Malware
	- Vulnerability discovered: `June 18th 2014`
	- Vulnerability reported: `July 16th 2014`
	- Vulnerability fixed in version `2.0.3` released on `October 3rd 2014`
- Malwarebytes Anti-Exploit
	- Vulnerablity discovered: `August 19th 2014`
	- Vulnerability reported: `August 21st 2014`
	- Vulnerability fixed in version `1.04.1.1012` released on `September 5th 2014`

### The vulnerability ###

Both Anti-Malware and Anti-Exploit have upgrade capabilities through the form of HTTP transfered installation packages. Both software packages have no or limited upgrade validation implemented thus allowing anyone who can work out the upgrade protocol to inject their own payload.
