# CVE-2020-29666
Directory Listing

[Suggested description]
In Lan ATMService M3 ATM Monitoring System 6.1.0, due to a directory listing vulnerability, a remote attacker can view log files, located in /websocket/logs/, that contain a user's cookie values and the predefined developer's cookie value.
------------------------------------------
[Additional Information]
A letter was sent to the vendor about the vulnerability.
------------------------------------------
[VulnerabilityType Other]
CWE-548: Exposure of Information Through Directory Listing
------------------------------------------
[Vendor of Product]
Lan ATMService LLC (http://lanatmservice.ru/)
------------------------------------------
[Affected Product Code Base]
Affected version: M3 ATM Monitoring System 6.1.0. There are no fixed versions and any response from developers.
------------------------------------------
[Affected Component]
Server misconfiguration, that allows to remote attacker view a user's cookie value in log files.
------------------------------------------
[Attack Type]
Remote
------------------------------------------
[Impact Information Disclosure]
true
------------------------------------------
[Attack Vectors]
A remote attacker can view log files, located in {HOST}/websocket/logs/, that contain a user's cookie values.
------------------------------------------
[Discoverer]
Dmitry Kuramin (Jet Infosystems, jet.su)
------------------------------------------
[Reference]
https://jet.su
