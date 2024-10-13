# CVE-2021-42559: Command Injection via Configurations in MITRE Caldera

Caldera (versions <=2.8.1) contains multiple startup "requirements" that execute commands when starting the server. Because these commands can be changed via the Rest API, an authenticated user can insert arbitrary commands that will execute when the server is restarted.
<br/>

### Vendor Disclosure:

The vendor's disclosure for this vulnerability can be found [here](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42559).

### Requirements:

This vulnerability requires:
<br/>
- Valid user credentials
- Waiting for the Caldera application to be restarted

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2021-42559/blob/main/Caldera%20-%20CVE-2021-42559.pdf).
