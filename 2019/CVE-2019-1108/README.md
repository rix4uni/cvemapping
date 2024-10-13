# CVE-2019-1108 Exploitation

```
CVE-2019-1108
Remote Desktop Protocol Client Information Disclosure Vulnerability
Published: 07/09/2019 | Last Updated : 11/19/2019
MITRE CVE-2019-1108

An information disclosure vulnerability exists when the Windows RDP client improperly discloses the contents of its memory. An attacker who successfully exploited this vulnerability could obtain information to further compromise the user’s system.

To exploit this vulnerability, an attacker would have to connect remotely to an affected system and run a specially crafted application.

The security update addresses the vulnerability by correcting how the Windows RDP client initializes memory.
```

![leak](./leak.png)
