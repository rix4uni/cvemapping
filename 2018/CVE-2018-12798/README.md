# Adobe Acrobat Reader Heap Overflow Remote Code Execution Vulnerability

# Vulnerability

Improper Restriction of Operations within the Bounds of a Memory Buffer Vulnerability


# Vulnerability Description

This vulnerability allows remote attackers to execute arbitrary code on vulnerable installations of Adobe Acrobat Pro DC. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the processing of unicode strings. When parsing, the process does not properly validate the length of user-supplied data prior to copying it to a fixed-length, heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process.


# CVE ID

CVE-2018-12798


# Vendor

www.adobe.com


# Product

* Acrobat DC 2018.011.20040 and prior
* Acrobat Reader DC 2018.011.20040 and prior
* Acrobat 2017 2017.011.30080 and prior
* Acrobat Reader 2017 2017.011.30080 and prior
* Acrobat DC 2015.006.30418 and prior
* Acrobat Reader DC 2015.006.30418 and prior


# Disclosure Timeline

1. 08 January 2018 - Reported to vendor
2. 10 July 2018 - Coordinated public release of advisory


# Credits

Ashfaq Ansari and Sudhakar Verma - Project Srishti


# Vendor Advisory

https://helpx.adobe.com/security/products/acrobat/apsb18-21.html
