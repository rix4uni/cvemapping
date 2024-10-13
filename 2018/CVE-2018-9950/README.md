# Foxit Reader PDF Parsing Out-Of-Bounds Read Information Disclosure Vulnerability

# Vulnerability

Improper Restriction of Operations within the Bounds of a Memory Buffer Vulnerability


# Vulnerability Description

This vulnerability allows remote attackers to disclose sensitive information on vulnerable installations of Foxit Reader. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PDF documents. The issue results from the lack of proper validation of user-supplied data, which can result in a read past the end of an allocated object. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of the current process.


# CVE ID

CVE-2018-9950


# Vendor

www.foxitsoftware.com


# Product

* Foxit Reader 8.3.5.30351 and prior
* Foxit PhantomPDF 8.3.5.30351 and prior


# Disclosure Timeline

1. 19 January 2018 - Reported to vendor
2. 20 April 2018 - Coordinated public release of advisory


# Credits

Sudhakar Verma and Ashfaq Ansari - Project Srishti


# Vendor Advisory

https://www.foxitsoftware.com/support/security-bulletins.php
