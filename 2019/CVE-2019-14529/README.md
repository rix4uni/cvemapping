# CVE-2019-14529
Multiple SQL Injection vulnerability in OpenEMR project

**Vulnerable function in file:** /openemr/interface/forms/eye_mag/save.php

**Conditions** : any authorized user

**Vulnerable versions:** <5.0.2, Fixed in 5.0.2 version.

## Description

There are two functions:
 1. "store_PDF", with non filtered variable "encounter",
 2. "canvas", with non two filtered variable "encounter" and "zone".
 
 Both functions use this variables in `DELETE` sql query without any filtration. Both variables controlled by attacker.
 
 Error messages contains code of SQL queries and SQL error message. It can be used for exploit `error-based` type of SQL Injection.
 
 ## Impact
 
 Disclosure of **VERY** sensitive information, since this software used in medical sphere.
 
 ## Other
 
 [OpenEMR official site](https://www.open-emr.org/)
 
 [OpenEMR git repo](https://github.com/openemr)
 
 [Patch for this issue](https://github.com/openemr/openemr/pull/2592)

*P.S. Special thanks to  Brady G. Miller from OpenEMR team for fast response and patches*
