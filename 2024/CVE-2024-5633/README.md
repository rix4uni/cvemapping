# PoC for CVE-2024-5633

Longse model LBH30FE200W cameras, as well as products based on this device, provide an unrestricted access for an attacker located in the same local network to an undocumented binary service CoolView on one of the ports.  An attacker with a knowledge of the available commands is able to perform read/write operations on the device's memory, which might result in e.g. bypassing telnet login and obtaining full access to the device.

https://www.cve.org/CVERecord?id=CVE-2024-5633