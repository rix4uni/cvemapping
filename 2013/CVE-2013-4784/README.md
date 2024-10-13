ipmitest
========

Shell script for testing the IPMI cipher type zero authentication bypass vulnerability (CVE-2013-4784)

The IPMI  is a standardized computer system interface used by system administrators for out-of-band management of computer
systems and monitoring of their operation. It is a way to manage a computer that may be powered off or otherwise unresponsive by using a network connection to the hardware
rather than to an operating system or login shell.

The vulnerability allows remote attackers to bypass authentication and execute arbitrary IPMI commands by using cipher suite 0 (aka cipher zero) 
and an arbitrary password.

Usage:

bash ipmitest.sh [target]

Example:

alexos@cypher:~$ bash ipmitest.sh 192.168.0.1

------------------------------------------------------
 
IPMITest - (0.2)

by Alexandro Silva - Alexos (alexos.org)

------------------------------------------------------ 


[*] Testing dependencies...


[*] ipmitool version 1.8.11.dell19 installed...


[*] Analyzing IPMI on 192.168.0.1...


[*] Testing for Zero Cipher (CVE-2013-4784)...

privilege level               : ADMINISTRATOR

console ip                    : 192.168.0.1

[*] done
