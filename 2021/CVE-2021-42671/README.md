# CVE-2021-42671
CVE-2021-42671 - Broken access control vulnerability in the Engineers online portal system. 

# Technical description:
A broken access control vulnerability exists in the Engineers Online Portal. An attacker can leverage this vulnerability in order to bypass access controls and get his hands on all the files uploaded to the web server without the need of authentication or authorization. 

Vulnerable domain - http://localhost/nia_munoz_monitoring_system/admin/uploads/

# Proof of concept (Poc) -
Navigate to http://localhost/nia_munoz_monitoring_system/admin/uploads/ in order to bypass the access control of the target web server. 
As a result you can reach sensetive information stored on the web server uploads folder. 

![CVE-2021-42671](https://user-images.githubusercontent.com/93016131/140196897-9f334ed2-a477-4b5e-a806-57a11d17a615.gif)

# References - 
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-42671

https://nvd.nist.gov/vuln/detail/CVE-2021-42671

# Discovered by - 
Alon Leviev(0xDeku), 22 October, 2021. 
