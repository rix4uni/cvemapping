# CVE-2023-29929: Remote "Instakill" DoS in Kemp LoadMaster via DNS Packet

Kemp LoadMaster devices (firmware < 7.2.60) suffer from a critical buffer overflow vulnerability in the isreverse() and locate_fqdn() methods of the libkemplink.so library. The vulnerability stems from an undersized 256-byte buffer allocated for DNS Names, which can be exploited by sending a specially crafted DNS request containing special or Unicode characters.

Successful exploitation leads to an immediate crash and denial-of-service (DoS) condition. The presence of a stack canary token prevents further exploitation, but the possibility of remote code execution (RCE) cannot be ruled out if an attacker finds another vulnerability to leak the stack canary token.

The vulnerability is easily triggered by sending a DNS request over TCP or UDP to the exposed DNS services of the LoadMaster device. A simple proof-of-concept is:
`dig @kempdeviceip 😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀😀😀.😀😀.com` (On some Linux flavors you'll need to add `+noidnout +noidnin`)

The exploit leverages a specific step in the DNS name resolution process. While the allocated buffer of 256 bytes is the standard maximum size for DNS Names transmitted over the network, and the proof-of-concept fits within this limit, the special and Unicode characters expand in size when escaped during processing. Thus, the buffer size after escaping exceeds the original allocation. The Bind9 library's documentation and source code (which the DNS component is forked from) indicates that a buffer of at least 1004 bytes is necessary for safe operation, with a conservative buffer size of 1023 bytes being recommended. For further details, see [here](https://github.com/isc-projects/bind9/blob/87942ee0b47240e5093642768983b3053cfdc01c/lib/dns/include/dns/name.h#L891).


Timeline:
* Feb-March 2023: Vuln discovered
* March 2023: Disclosed to vendor
* Mar 20, 2023: Vendor acknowledged and reproduced the vulnerability
* May 15, 2023: Vendor confirmed fix "In Development" with assigned dev ticket LM-2446
* July 17, 2024: Vendor released fix version 7.2.60.0, see https://docs.progress.com/bundle/release-notes_loadmaster-7-2-60-0/page/Issues-Resolved.html
* Aug 21, 2024: Previously reserved CVE published to https://www.cve.org/CVERecord?id=CVE-2023-29929
