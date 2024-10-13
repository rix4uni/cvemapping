# CVE-2021-42756

Multiple stack-based buffer overflow vulnerabilities [CWE-121] in the proxy daemon of FortiWeb 5.x all versions, 6.0.7 and below, 6.1.2 and below, 6.2.6 and below, 6.3.16 and below, 6.4 all versions may allow an unauthenticated remote attacker to achieve arbitrary code execution via specifically crafted HTTP requests.

## Summary

When MitB protection is enabled, there is no limit to the length of the protected fields. This can lead to a stack overflow.

## PoC

Environment: FortiWeb 6.3.4

<img src="https://github.com/3ndorph1n/CVE-2021-42756/blob/main/poc.png" style="zoom: 67%;" />

## References

* [PSIRT Advisories | FortiGuard](https://www.fortiguard.com/psirt/FG-IR-21-186)
