# CVE-2024-2188

CVE-2024-2188 is a Stored XSS vulnerability in the TP-Link Archer AX50 router, affecting firmware version 1.0.11 build 2022052.
It occurs in the UPnP service, where command `AddPortMapping` allows attackers to create a new `PortMapping` entry without sanitizing user input for the `description` field.
This allows the attacker to inject HTML entities with malicious JavaScript that will be executed when visiting the tha UPnP tab in the NAT Forwarding admin page (`Advanced > NAT Forwarding > UPnP`).
If an authenticated user triggers the XSS, it allows an unatuthenticated attacker to perform actions as that authenticated user, potentially allowing further compromise of the device
