# Boot Hole Fix

This script will remediate the BootHole bug identified in CVE-2020-25632 and/or CVE-2021-20233.

On July 29, 2020, Microsoft published security advisory 200011 that describes a new vulnerability that's related to Secure Boot.

Devices that trust the Microsoft third-party Unified Extensible Firmware Interface (UEFI) Certificate Authority (CA) in their Secure Boot configuration may be susceptible to an attacker who has administrative privileges or physical access to the device.

This script is to apply the latest Secure Boot DBX revocation list to invalidate the vulnerable modules. 

Paul Rowland - 2022

v1.0 - 19/07/2022

Steps for use:

1) Download the latest BootHoleFix.ps1 file and save it to a location such as "C:\Users\\%UserName%\Desktop".
2) Launch PowerShell as an admin.
3) Navigate to the directory above (typing "cd C:\Users\\%UserName%\Desktop").
4) Type ".\BootHoleFix.ps1" and hit Enter.
5) Close the window when the "Complete, you may now close this window..." message appears in green
