# CVE-2020-13259
PoC of Full Account Takeover on RAD SecFlow-1v 

A vulnerability in the web-based management interface of RAD SecFlow-1v could allow an unauthenticated, remote attacker to conduct a cross-site request forgery (CSRF) attack on an affected system.
The vulnerability is due to insufficient CSRF protections for the web UI on an affected device.
An attacker could exploit this vulnerability by persuading a user of the interface to follow a malicious link. A successful exploit could allow the attacker to perform arbitrary actions with the privilege level of the affected user.
This could be exploited in conjunction with CVE-2020-13260.

# Proof of Concept
By persuading an authenticated user to open a web page containing a JS code.
This attack could execute any operation available at the web-based management interface (File uploads, Scheduled reboot, Factory reset etc.)

# Full Account Takeover
As mentioned above, this exploit could be used in conjunction with CVE-2020-13260 (Stored-XSS), by using the CSRF exploit to upload a malicious file to a Stored-XSS vulnerabale page, which could allow full-account takeover.

Please view Poc.html file.


