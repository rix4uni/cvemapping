# CVE-2018-8090

# DLL Hijacking in Quickheal Total Security/ Internet Security/ Antivirus Pro (Installers)

### Affected Products:
  - Quick Heal Total Security - 17.00
  - Quick Heal Internet Security - 17.00
  - Quick Heal AntiVirus Pro - 17.00

### Affected Installers:
  - Quick Heal Total Security 64 bit 17.00 (QHTS64.exe), (QHTSFT64.exe)    - Version 10.0.1.38
  - Quick Heal Total Security 32 bit 17.00 (QHTS32.exe), (QHTSFT32.exe)    - Version 10.0.1.38
  - Quick Heal Internet Security 64 bit 17.00 (QHIS64.exe), (QHISFT64.exe) - Version 10.0.0.37 
  - Quick Heal Internet Security 32 bit 17.00 (QHIS32.exe), (QHISFT32.exe) - Version 10.0.0.37
  - Quick Heal AntiVirus Pro 64 bit 17.00 (QHAV64.exe), (QHAVFT64.exe)     - Version 10.0.0.37
  - Quick Heal AntiVirus Pro 32 bit 17.00 (QHAV32.exe), (QHAVFT32.exe)     - Version 10.0.0.37
    
All of the above installers allow DLL hijacking due to insecure library loading. As all these installers require admin privileges so it is possible load and execute code with admin privileges.

DLL's that can be loaded in 32 bit versions:
  - cryptsp.dll
  - cryptnet.dll
  - cryptbase.dll
  - gpapi.dll
  - ncrypt.dll
  - profapi.dll
  - sensapi.dll
  - userenv.dll
  
DLL's that can be loaded in 64 bit versions:
  - cryptsp.dll
  - cryptbase.dll
  - iphlpapi.dll
  
## Timeline:
  - 04/Dec/2017  - Reported Vulnerability to Quickheal
  - 25/Dec/2017  - Quickheal acknowledged the Vulnerability
  - 27/Apr/2018  - Vulnerability Fixed (Version of Total Security - 10.0.1.46)
  - 23/July/2018 - Bounty Recieved (30,000 rupees)
  
## Additional Links
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-8090

https://nvd.nist.gov/vuln/detail/CVE-2018-8090
