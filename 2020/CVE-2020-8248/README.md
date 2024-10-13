# CVE-2020-8248: Privilege Escalation via Zip Wildcard Exploit in Pulse Secure VPN Linux Client

The root SUID executable pulsesvc, has a function “do_upload” that unsafely calls a zip command with wildcards (“*”). By writing files with specifically crafted names, in a user- controlled folder (“~/.pulse_secure/pulse/”), an attacker can abuse the wildcards in order to pass custom flags to the “zip” executable resulting in code execution.

### NVD Disclosure:

The NVD disclosure for this vulnerability can be found [here](https://nvd.nist.gov/vuln/detail/CVE-2020-8248).

### Requirements:

The exploit targets code that is accessed post client authentication, that means that in order to exploit this vulnerability an attacker would require one of the 3 scenarios:
- Hosting an attacker-controlled Pulse VPN Server
- A valid SSL/TLS certificate to host a dummy VPN server (Can be easily done with
solutions such as “Let’s Encrypt”)
- Connecting to a legitimate Pulse VPN Server (User credentials/Client certificates
may be found directly on the compromised client)

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2020-8248/blob/main/Pulse%20Secure%20VPN%20Linux%20Client%20-%20CVE-2020-8248.pdf).
