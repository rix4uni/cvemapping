# CVE-2020-8250: Privilege Escalation via Command Injection in Pulse Secure VPN Linux Client

The root SUID executable pulsesvc, has a function “do_upload” that unsafely passes the “HOME” environmental variable to “system()”. By altering the “HOME” variable to contain special shell characters (Ex: “``” or “$()”), an attacker can inject arbitrary commands when “do_upload” is called and can elevate his/her privileges to root.

### NVD Disclosure:

The ND disclosure for this vulnerability can be found [here](https://nvd.nist.gov/vuln/detail/CVE-2020-8250).

### Requirements:

The exploit targets code that is accessed post client authentication, that means that in order to exploit this vulnerability an attacker would require one of the 3 scenarios:
- Hosting an attacker-controlled Pulse VPN Server
- A valid SSL/TLS certificate to host a dummy VPN server (Can be easily done with solutions such as “Let’s Encrypt”)
- Connecting to a legitimate Pulse VPN Server (User credentials/Client certificates may be found directly on the compromised client)

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2020-8250/blob/main/Pulse%20Secure%20VPN%20Linux%20Client%20-%20CVE-2020-8250.pdf).
