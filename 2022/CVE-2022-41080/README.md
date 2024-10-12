# CVE-2022-41080

## Desc

- CrowdStrike recently discovered a new exploit method (called OWASSRF) consisting of CVE-2022-41080 and CVE-2022-41082 to achieve remote code execution (RCE) through Outlook Web Access (OWA). The new exploit method bypasses URL rewrite mitigations for the Autodiscover endpoint provided by Microsoft in response to ProxyNotShell.
- The discovery was part of recent CrowdStrike Services investigations into several Play ransomware intrusions where the common entry vector was confirmed to be Microsoft Exchange.
- After initial access via this new exploit method, the threat actor leveraged legitimate Plink and AnyDesk executables to maintain access, and performed anti-forensics techniques on the Microsoft Exchange server in an attempt to hide their activity.

## Poc

![Poc](./Poc.png)

## More

[https://www.crowdstrike.com/blog/owassrf-exploit-analysis-and-recommendations/](https://www.crowdstrike.com/blog/owassrf-exploit-analysis-and-recommendations/)
