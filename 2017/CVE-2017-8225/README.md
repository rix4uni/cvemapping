# CVE-2017-8225 - GoAhead System.ini Leak

This vulnerability pertains to Wireless IP Camera (P2P) WIFICAM devices. It arises from a lapse in correctly validating .ini files, which store critical credentials. An adept attacker can exploit this by providing empty values for both the loginuse and loginpas parameters in the URI. Specifically, access is granted via the path: /system.ini?loginuse&loginpas.

# Exploit Details

For demonstration purposes, a Proof-of-Concept (PoC) exploit has been provided. However, it is essential to exercise extreme caution and ensure proper authorization before employing this exploit.

# Disclaimer

This PoC exploit is intended solely for educational and testing purposes. Unauthorized use may contravene legal regulations in your jurisdiction. The author bears no responsibility for any misuse or consequential damages arising from the application of this exploit.
