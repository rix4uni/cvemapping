# Foxit Reader CPDF_Object Use-After-Free Remote Code Execution Vulnerability

# Vulnerability

Referencing memory after it has been freed can cause a program to crash, use unexpected values, or execute code


# Vulnerability Description

This vulnerability allows remote attackers to execute arbitrary code on vulnerable installations of Foxit Reader. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the handling of CPDF_Object objects. The issue results from the lack of validating the existence of an object prior to performing operations on the object. An attacker can leverage this vulnerability to execute code under the context of the current process.


# CVE ID

CVE-2018-9951


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
