# CVE-2017-7308

**CVE ID:** CVE-2017-7308

**Publish date:** 2017-03-29T20:59:00.373

**Base score (CVSS 3.0/3.1):** 7.8

**Description:** The packet_set_ring function in net/packet/af_packet.c in the Linux kernel through 4.10.6 does not properly validate certain block-size data, which allows local users to cause a denial of service (integer signedness error and out-of-bounds write), or gain privileges (if the CAP_NET_RAW capability is held), via crafted system calls.
