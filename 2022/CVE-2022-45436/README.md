# CVE-2022-45436
Reflected Cross Site Scripting leading to session hijacking in pandorafms <= Package v765 RRR.

#### > Exploit Title: Reflected Cross Site Scripting
#### > Date: 15/02/2023
#### > Exploit Author: Damodar Naik
#### > Vendor Homepage: https://pandorafms.com/en/
#### > Software Link: https://github.com/pandorafms/pandorafms
#### > Version: <= v765 RRR
#### > Tested on: Ubuntu
#### > CVE ID: CVE-2022-45436


### Steps to reproduce

Get the request by hitting the help button in the "http://localhost:8080/pandora_console/index.php?sec=network&sec2=operation/agentes/pandora_networkmap". (As shown in POC).
    Add the payload in the "b" parameter in the request.
    Copy the URL with payload in it, and it to the user logged in as admin.
    When Admin user try to visit the malicious link payload will gets executed.
XSS payload will be executed, which could be used for stealing admin users cookie value, etc.
