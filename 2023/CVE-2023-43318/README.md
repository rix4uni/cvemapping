# CVE-2023-43318

## JetStream Smart Switch - TL-SG2210P v5.0/ Improper Access Control / CVE-2023-43318

[+] Credits: Shahnawaz Shaikh, Security Researcher at Cybergate Defense LLC


[+] [Twitter](twitter.com/_striv3r_)


### Vendor:
Tp-Link (http://tp-link.com)


### Product:
JetStream Smart Switch - TL-SG2210P


### Vulnerability Type:
Incorrect Access Control (DOS)


### Affected Product Code Base:
JetStream Smart Switch - TL-SG2210P 5.0 Build 20211201


### Affected Component:
usermanagement, swtmactablecfg endpoints


### Security Issue:
TP-Link JetStream Smart Switch TL-SG2210P 5.0 Build 20211201 allows attackers to escalate privileges via modification of the 'tid' and 'usrlvl' values in GET requests.


### Attack Vectors:
A successful breach could grant improper admin controls, potentially compromising the system. Lower privilege users can access admin level endpoints via their own token ID.


### CVE Reference:
CVE-2023-43318


### Network Access:
Remote


### Severity:
High


### Disclosure Timeline: 
Vendor Notification: September 12, 2023
Vendor released fixed firmware TL-SG2210P(UN)_V5.20_5.20.1 Build 20240202: February 29, 2024
March 1, 2024 : Public Disclosure
