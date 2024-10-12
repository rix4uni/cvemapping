# ofbiz-CVE-2023-49070-RCE-POC

This is a pre-auth RCE POC For CVE-2023-49070 which affected Apache ofbiz applications < 18.12.10 due to xml-rpc java deserialzation bug. <br>
for more information please refer to : https://github.com/advisories/GHSA-9rm6-p86c-42xm <br>

dockered vulnerable ofbiz image : https://hub.docker.com/r/marcopinball/ofbiz-demo

## You must download ysoserial-all.jar from here <br>
> wget https://github.com/frohoff/ysoserial/releases/latest/download/ysoserial-all.jar

### Dns POC
![image](https://github.com/abdoghazy2015/ofbiz-CVE-2023-49070-RCE-POC/assets/64314534/052bfe16-401b-40cc-be19-17b48fd3b81a)

### RCE POC

![image](https://github.com/abdoghazy2015/ofbiz-CVE-2023-49070-RCE-POC/assets/64314534/c66708ea-4f6a-4c8e-829f-222d74d59962)

#### This tweets helped me alot : 
- https://twitter.com/Siebene7/status/1731870759130427726
- https://twitter.com/_0xf4n9x_/status/1732289811665559775

This exploit has been developed by Abdelhameed Ghazy. <br>
Twitter : https://twitter.com/abd0ghazy
Linkedin : https://www.linkedin.com/in/abdelhameed-ghazy-1a50b619a/
