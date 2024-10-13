### CVE-2020-17382 Windows 10 x64 2004 Build 19041.264 Exploit

Kudos to [@matteomalvica](https://twitter.com/matteomalvica) for asking me so many questions about this vulnerability that forced me to write an exploit for him for the latest Windows 10 release 19041.264 without KVA Shadow (i.e. non Specter vulnerable CPUs) and without VBS. Trivial to adapt to older Windows versions (Matteo adapted it to 1709, check his blog [post](https://www.matteomalvica.com/blog/2020/09/24/weaponizing-cve-2020-17382/)).

On CPUs vulnerable to [CVE-2018-3620](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/ADV180018) it becomes tricky because your ROP chain will grow considerably to make the PML4 executable, and you will end up overwriting stack cookies of the **ntoskrnl** function where you "want" to return.

Credits and original advisory here https://www.coresecurity.com/core-labs/advisories/msi-ambient-link-multiple-vulnerabilities
