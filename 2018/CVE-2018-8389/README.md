# jscript.dll - ActiveXObject BSTR - Use After Free

# Vulnerability

Referencing memory after it has been freed can cause a program to crash, use unexpected values, or execute code.


# Vulnerability Description

A remote code execution vulnerability exists in the way that the scripting engine handles objects in memory in Internet Explorer. The vulnerability could corrupt memory in such a way that an attacker could execute arbitrary code in the context of the current user. An attacker who successfully exploited the vulnerability could gain the same user rights as the current user. If the current user is logged on with administrative user rights, an attacker who successfully exploited the vulnerability could take control of an affected system. An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights.


# CVE ID

CVE-2018-8389


# Vendor

www.microsoft.com


# Product

jscript.dll


# Disclosure Timeline

1. 09 January 2018 - Reported to vendor
2. 14 August 2018 - Coordinated public release of advisory


# Credits

Sudhakar Verma and Ashfaq Ansari - Project Srishti


# Vendor Advisory

https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2018-8389
