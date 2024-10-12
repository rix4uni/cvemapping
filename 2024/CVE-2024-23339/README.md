# CVE-2024-23339



## 취약점 개요

- CVE-2024-23339

- CVSS : 6.5

- Jan 23, 2024

- ProtoType Pollution in node.js package

- rebob 프로젝트의 일환



## 취약점 설명

[github advisories](https://github.com/advisories/GHSA-4c2g-hx49-7h25)


hoolock is a suite of lightweight utilities designed to maintain a small footprint when bundled. Starting in version 2.0.0 and prior to version 2.2.1, utility functions related to object paths (`get`, `set`, and `update`) did not block attempts to access or alter object prototypes. Starting in version 2.2.1, the `get`, `set` and `update` functions throw a `TypeError` when a user attempts to access or alter inherited properties.


**Impact**

Utility functions related to object paths (get, set and update) did not block attempts to access or alter object prototypes.

***Patches**

The get, set and update functions will throw a TypeError when a user attempts to access or alter inherited properties in versions >=2.2.1.


