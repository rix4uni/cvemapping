# McAfee Virus Scan for Linux multiple remote flaws
[![Docker Pulls](https://img.shields.io/docker/pulls/vulnerables/exploit-CVE-2016-8016-25.svg?style=plastic)](https://hub.docker.com/r/vulnerables/exploit-CVE-2016-8016-25/)

> THIS EXPLOIT AND ALL THE CODE IN THIS REPO WERE REMOVED TO AVOID ANY PROBLEMS REGARDING VIOLATING ANY MCAFEE LICENSE

McAfee VirusScan Enterprise for Linux is a enterprise antivirus solution by Mcafee. Its unique, Linux-based on- access scanner constantly monitors the system for potential attacks.

### Flaws

VSEL 2.0.3 (and earlier) is vulnerable to the following published security vulnerabilities. The ENSL 10.2 release resolves the following vulnerabilities. Intel Security highly recommends that all customers upgrade from VSEL to ENSL.

 * CVE-2016-8016: Information Exposure in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows authenticated remote attackers to obtain the existence of unauthorized files on the system via a URL parameter.
 * CVE-2016-8017: Special Element Injection in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows authenticated remote attackers to read files on the webserver via a crafted user input.
 * CVE-2016-8018: Cross Site Request Forgery (CSRF) in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows authenticated remote attackers to execute unauthorized commands via a crafted user input.
 * CVE-2016-8019: Cross-Site Scripting (XSS) in Attributes in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows unauthenticated remote attackers to inject arbitrary web script or HTML via a crafted user input.
 * CVE-2016-8020: Improper Control of Generation of Code in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows remote authenticated users to execute arbitrary code via a crafted HTTP request parameter.
 * CVE-2016-8021: Improper Verification of Cryptographic Signature in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows remote authenticated users to spoof update server and execute arbitrary code via a crafted input file.
 * CVE-2016-8022: Authentication Bypass by Spoofing in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows remote unauthenticated attacker to execute arbitrary code or cause a denial of service via a crafted cookie.
 * CVE-2016-8023: Authentication Bypass by Assumed-Immutable Data in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows remote unauthenticated attacker to bypass server authentication via a crafted cookie.
 * CVE-2016-8024: Improper Neutralization of CRLF Sequences in HTTP Headers in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows remote unauthenticated attacker to obtain sensitive information via the server HTTP response spoofing.
 * CVE-2016-8025: SQL Injection in Intel Security McAfee VirusScan Enterprise Linux 2.0.3 (and earlier) allows remote authenticated users to obtain product information via a crafted HTTP request parameter.

### Vulnerable versions

VirusScan Enterprise for Linux (VSEL) 2.0.3 and earlier

### Credits

This flaw was found by Andrew Fasan.

### Copyright 

AVERT, EPO, EPOLICY ORCHESTRATOR, FOUNDSTONE, GROUPSHIELD, INTRUSHIELD, LINUXSHIELD, MAX (MCAFEE SECURITYALLIANCE EXCHANGE), MCAFEE, NETSHIELD, PORTALSHIELD, PREVENTSYS, SECURITYALLIANCE, SITEADVISOR, TOTAL PROTECTION, VIRUSSCAN, WEBSHIELD are registered trademarks or trademarks of McAfee, Inc. and/or its affiliates in the US and/or other countries. McAfee Red in connection with security is distinctive of McAfee brand products. All other registered and unregistered trademarks herein are the sole property of their respective owners.

### Disclaimer

This or previous program is for Educational purpose ONLY. Do not use it without permission. The usual disclaimer applies, especially the fact that me (opsxcq) is not liable for any damages caused by direct or indirect use of the information or functionality provided by these programs. The author or any Internet provider bears NO responsibility for content or misuse of these programs or any derivatives thereof. By using these programs you accept the fact that any damage (dataloss, system crash, system compromise, etc.) caused by the use of these programs is not opsxcq's responsibility.
