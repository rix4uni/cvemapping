# CVE-2022-43980
Stored Cross Site Scripting Vulnerability in the network maps edit functionality of PandoraFMS <= Package v765 RRR.



##### > Exploit Title: Stored Cross Site Scripting
##### > Date: 15/02/2023
##### > Exploit Author: Gaurish Kauthankar
##### > Vendor Homepage: https://pandorafms.com/en/
##### > Software Link: https://github.com/pandorafms/pandorafms
##### > Version: <= v765 RRR
##### > Tested on: Ubuntu
##### > CVE ID: CVE-2022-43980


### Steps to reproduce
1. As a low privilege user, create a network map containing name as xss payload.  
2. Once created, admin user must click on the edit network maps link.  
3. XSS payload will be executed, which could be used for stealing admin users cookie value, etc.
