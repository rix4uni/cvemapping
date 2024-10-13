# CVE-2021-41160

FreeRDP is a free implementation of the Remote Desktop Protocol (RDP), released under the Apache license. In affected versions a malicious server might trigger out of bound writes in a connected client. Connections using GDI or SurfaceCommands to send graphics updates to the client might send `0` width/height or out of bound rectangles to trigger out of bound writes. With `0` width or heigth the memory allocation will be `0` but the missing bounds checks allow writing to the pointer at this (not allocated) region. This issue has been patched in FreeRDP 2.4.1.

| authentication | complexity | vector |
| --- | --- | --- |
| NONE | MEDIUM | NETWORK |

| confidentiality | integrity | availability |
| --- | --- | --- |
| PARTIAL | PARTIAL | PARTIAL |

## CVSS Score: **6.8**

## References

* https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-7c9r-6r2q-93qg

* https://lists.fedoraproject.org/archives/list/package-announce@lists.fedoraproject.org/message/DWJXQOWKNR7O5HM2HFJOM4GBUFPTE3RG/

* https://lists.fedoraproject.org/archives/list/package-announce@lists.fedoraproject.org/message/ZXCR73EDVPLI6TRWRAWJCJ7OBYDKBB74/

* https://lists.fedoraproject.org/archives/list/package-announce@lists.fedoraproject.org/message/WIZUPVRGCWUDAPDOQVUGUIYUO7UWKMXX/

* https://security.gentoo.org/glsa/202210-24

## Brut File

* [CVE-2021-41160.json](./data_brut.json)



## About this repository
This repository is part of the project [Live Hack CVE](https://github.com/Live-Hack-CVE). Made by [Sn0wAlice](https://github.com/Sn0wAlice) for the people that care about security and need to have a feed of the latest CVEs. Hope you enjoy it, don't forget to star the repo and follow me on [Twitter](https://twitter.com/Sn0wAlice) and [Github](https://github.com/Sn0wAlice)