# CVE-2021-34767
## Description

Cisco IOS XE Software for Catalyst 9800 Series Wireless Controllers IPv6 Denial of Service Vulnerability

A vulnerability in IPv6 traffic processing of Cisco IOS XE Wireless Controller Software for Cisco Catalyst 9000 Family Wireless Controllers could allow an unauthenticated, adjacent attacker to cause a Layer 2 (L2) loop in a configured VLAN, resulting in a denial of service (DoS) condition for that VLAN. The vulnerability is due to a logic error when processing specific link-local IPv6 traffic. An attacker could exploit this vulnerability by sending a crafted IPv6 packet that would flow inbound through the wired interface of an affected device. A successful exploit could allow the attacker to cause traffic drops in the affected VLAN, thus triggering the DoS condition.

## CVSS Score
7.4

## Reference
https://nvd.nist.gov/vuln/detail/CVE-2021-34767
https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ewlc-ipv6-dos-NMYeCnZv
https://bst.cloudapps.cisco.com/bugsearch/bug/CSCvw18506

## Notes
Published by Cisco, they were great to work with and in fixing the issue. 

I'm listed as the source.
