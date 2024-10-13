# CVE-2020-29667
Insufficient Session Expiration | Predefined Cookie Value

[Suggested description]
In Lan ATMService M3 ATM Monitoring System 6.1.0, a remote attacker able to use a default cookie value, such as PHPSESSID=LANIT-IMANAGER, can achieve control over the system and operate remote ATM maschines current state, because of Insufficient Session Expiration and Predefined Cookie Value.
------------------------------------------
[Additional Information]
A letter was sent to the vendor about the vulnerability.
------------------------------------------
[VulnerabilityType Other]
CWE-613: Insufficient Session Expiration
------------------------------------------
[Vendor of Product]
Lan ATMService LLC (http://lanatmservice.ru/)
------------------------------------------
[Affected Product Code Base]
Affected version: M3 ATM Monitoring System 6.1.0. There are no fixed versions and any response from developers.
------------------------------------------
[Affected Component]
Application misconfiguration, that allows to remote attacker use a hardcoded predefined cookie value.
------------------------------------------
[Attack Type]
Remote
------------------------------------------
[Impact Information Disclosure]
true
------------------------------------------
[Impact Loss of Integrity]
Low
------------------------------------------
[Impact Loss of Availability]
High
------------------------------------------
[Attack Vectors]
A remote attacker can use a predefined cookie value for control over the system for operate ATM machines current state.
------------------------------------------
[Discoverer]
Dmitry Kuramin (Jet Infosystems, jet.su)
------------------------------------------
[Reference]
https://jet.su
