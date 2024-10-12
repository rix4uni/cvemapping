# CVE-2022-47373
Reflected Cross Site Scripting Vulnerability in PandoraFMS <= v766


##### > Exploit Title: Reflected Cross Site Scripting
##### > Date: 15/02/2023
##### > Exploit Author: Gaurish Kauthankar
##### > Vendor Homepage: https://pandorafms.com/en/
##### > Software Link: https://github.com/pandorafms/pandorafms
##### > Version: <= v766
##### > Tested on: Ubuntu
##### > CVE : CVE-2022-47373


### Steps to reproduce:  
1. Add xss payload in the search functionality present in module library section.  
2. Observe payload execution.  
3. Now share the url containing xss payload with the victim user to steal cookies, redirecting to evil website, etc.
