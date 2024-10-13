# CVE-2006-20001

A carefully crafted If: request header can cause a memory read, or write of a single zero byte, in a pool (heap) memory location beyond the header value sent. This could cause the process to crash. This issue affects Apache HTTP Server 2.4.54 and earlier.

| authentication | complexity | vector |
| --- | --- | --- |
| not available | not available | not available |

| confidentiality | integrity | availability |
| --- | --- | --- |
| not available | not available | not available |

## CVSS Score: **not available**

## References

* https://httpd.apache.org/security/vulnerabilities_24.html

## Brut File

* [CVE-2006-20001.json](./data_brut.json)



## About this repository
This repository is part of the project [Live Hack CVE](https://github.com/Live-Hack-CVE). Made by [Sn0wAlice](https://github.com/Sn0wAlice) for the people that care about security and need to have a feed of the latest CVEs. Hope you enjoy it, don't forget to star the repo and follow me on [Twitter](https://twitter.com/Sn0wAlice) and [Github](https://github.com/Sn0wAlice)