# CVE-2019-3929
Crestron/Barco/Extron/InFocus/TeqAV Remote Command Injection (CVE-2019-3929) Metasploit Module

Per [Tenable's description](https://www.tenable.com/security/research/tra-2019-20):

"A remote, unauthenticated attacker can execute operating system commands as root via crafted requests to the HTTP endpoint file_transfer.cgi. This vulnerability appears to affect all known devices including the Crestron AM-100 firmware 1.6.0.2, Crestron AM-101 firmware 2.7.0.1, Barco wePresent WiPG-1000 firmware 2.3.0.10, Barco wePresent WiPG-1600 before firmware 2.4.1.19, Extron ShareLink 200/250 firmware 2.0.3.4, Teq AV IT WIPS710 firmware 1.1.0.7, SHARP PN-L703WA firmware 1.4.2.3, Optoma WPS-Pro firmware 1.0.0.5, Blackbox HD WPS firmware 1.0.0.5, InFocus LiteShow3 firmware 1.0.16, and InFocus LiteShow4 2.0.0.7"

All credit to Tenable. Module successfully exploited Crestron AM-100/101 devices with firmware <= to that mentioned above.
