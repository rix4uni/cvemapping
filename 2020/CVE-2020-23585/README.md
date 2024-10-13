# CVE-2020-23585

**OPTILINK E-PON "MODEL NO: OP-XT71000N" with "HARDWARE VERSION: V2.2"; & "FIRMWARE VERSION: OP_V3.3.1-191028"**  

A remote attacker can conduct a cross-site request forgery (CSRF) attack on "OPTILINK OP-XT71000N Hardware Version: V2.2 , Firmware Version: OP_V3.3.1-191028". The vulnerability is due to insufficient CSRF protections for the "mgm_config_file.asp" because of which attacker can create a crafted "csrf form" which sends " malicious xml data" to "/boaform/admin/formMgmConfigUpload". the exploit allows attacker to "gain full privileges" and to "fully compromise of router & network".

**TARGET**

/mgm_config_file.asp

**Attack Vector**

"mgm_config_file.asp" allows to Save config file and to Uplode config file (file is in "XML format" which contains the "usernames & passwords" of "PPP, Telnet, Snmp, Ftp, login.asp" etc.. and other credentials). An attacker could exploit this vulnerability by persuading a user of the interface to follow a malicious link. A successful exploit could allow the attacker to perform arbitrary actions with the privilege level of the targeted user. the attacker could alter the configuration, execute commands, or reload an affected device.


**REGARDS**

Huzaifa Hussain

https://twitter.com/disguised_noob

https://www.linkedin.com/in/huzaifa-hussain-046791179
