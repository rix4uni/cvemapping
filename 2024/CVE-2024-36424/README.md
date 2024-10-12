# CVE-2024-36424

This vulnerability was discovered and disclosed by **M. Akil Gündoğan** from **Secunnix Vulnerability Research Team**. This repository will hold the proof-of concept and advisories.

# Details:

- **Product:** K7 Ultimate Security
- **Affected versions:** < v17.0.2019
- **CVE ID:** CVE-2024-36424
- **Operating System:** All supported Windows versions, tested on Windows 10 Pro
- **State:** Coordianted responsible disclosure.
- **Release Date:** 13.08.2024

# Vulnerability Description:

In **K7 Ultimate Security < v17.0.2019**, the driver file **(K7RKScan.sys - this version 15.1.0.7)** allows local users to cause a denial of service (BSOD) or possibly have unspecified other impact because of null pointer dereference from IOCtl **0x222010** and **0x222014**. At the same time, the drive is accessible to all users in the "Everyone" group. 

Technical details and step by step Proof of Concept's (PoC):

    1 - Install the driver in the path "C:\Program Files (x86)\K7 Computing\K7TSecurity\K7TSecurity\64Bit\K7RKScan.sys" to the system via OSRLoader or sc create.
    2 - Compile the attached PoC code written in C++ as release on VS 2022. 
    3 - Run the compiled PoC directly with a double click. You will see the system crash/BSOD.

Tested on: Windows 10 Pro x64, 22H2

![](/screenshot.png)

# Impact:

An attacker with unauthorized user access can cause the entire system to crash and terminate critical processes, including any antivirus process where the relevant driver is activated and used on the system.

# Advisories:

K7 Computing recommends that all customers update their products to the corresponding versions shown below:

K7 Ultimate Security (17.0.2019 or Higher)

# Timeline:

- 16.05.2024 - Vulnerability reported.
- 05.08.2024 - Vendor has fixed the vulnerability.
- 13.08.2024 - Released.

# References:

- Vendor: https://www.k7computing.com
- Advisory: https://support.k7computing.com/index.php?/selfhelp/view-article/Advisory-issued-on-5th-aug-2024-417
- CVE: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-36424
