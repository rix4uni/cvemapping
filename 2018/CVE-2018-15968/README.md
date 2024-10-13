# Adobe Reader Out-Of-Bounds Read Information Disclosure Vulnerability

# Vulnerability

Improper Restriction of Operations within the Bounds of a Memory Buffer Vulnerability


# Vulnerability Description

This vulnerability allows remote attackers to disclose sensitive information on vulnerable installations of Adobe Reader. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious PDF file.

The specific flaw exists within the parsing of **malformed PDF** file.  The issue results from the lack of proper validation of user-supplied data which can result in a read past the end of an allocated object. An attacker can leverage this in conjunction with other vulnerabilities to **execute code** in the context of the current process.


# CVE ID

CVE-2018-15968


# Vendor

www.adobe.com


# Product

* Acrobat DC 2018.011.20063 and prior
* Acrobat Reader DC 2018.011.20063 and prior
* Acrobat 2017 2017.011.30102 and prior
* Acrobat Reader 2017.011.30102 and prior
* Acrobat DC 2015.006.30452 and prior
* Acrobat Reader DC 2015.006.30452 and prior


# Disclosure Timeline

1. 08 January 2018 - Reported to vendor
2. 01 October 2018 - Coordinated public release of advisory


# Credits

Ashfaq Ansari - Project Srishti


# Vendor Advisory

https://helpx.adobe.com/security/products/acrobat/apsb18-30.html
