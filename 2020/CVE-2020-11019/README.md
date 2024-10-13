# CVE-2020-11019

In FreeRDP less than or equal to 2.0.0, when running with logger set to "WLOG_TRACE", a possible crash of application could occur due to a read of an invalid array index. Data could be printed as string to local terminal. This has been fixed in 2.1.0.

| authentication | complexity | vector |
| --- | --- | --- |
| SINGLE | LOW | NETWORK |

| confidentiality | integrity | availability |
| --- | --- | --- |
| NONE | NONE | PARTIAL |

## CVSS Score: **4**

## References

* https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-wvrr-2f4r-hjvh

* http://lists.opensuse.org/opensuse-security-announce/2020-07/msg00080.html

## Brut File

* [CVE-2020-11019.json](./data_brut.json)



## About this repository
This repository is part of the project [Live Hack CVE](https://github.com/Live-Hack-CVE). Made by [Sn0wAlice](https://github.com/Sn0wAlice) for the people that care about security and need to have a feed of the latest CVEs. Hope you enjoy it, don't forget to star the repo and follow me on [Twitter](https://twitter.com/Sn0wAlice) and [Github](https://github.com/Sn0wAlice)