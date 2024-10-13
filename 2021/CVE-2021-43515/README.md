# CVE-2021-43515 - Kimai 2 < v1.14 CSV Injection

Kimai is a free, open source and online time-tracking software designed for small businesses and freelancers. Same as any other collaboration project, it gives the users the ability to export data in several formats CSV, PDF, and HTML. However, it didn't properly sanatize the user input, which made room for potential injections. 

CSV Injection, also known as Formula Injection, occurs when websites embed untrusted input inside CSV files. On the dashboard page after a successful login, it is possible for an attacker to set certain values in the **Descreption** field that - when exported and opened with a spreadsheet application (Microsoft Excel, Open Office, etc.) - will be interpreted as a formula. This puts the users/administrators who open those malicious exported files at risk. Exfiltration of sensitive data or even the **execution of arbitrary code** on the local machine of the victim will be the result. The final impact depends on the used spreadsheet software on the client of the victim.

## PoC


![image](https://user-images.githubusercontent.com/32583633/164052927-be89f061-6c42-4880-b1c0-7b23576c680f.png)

![image](https://user-images.githubusercontent.com/32583633/164053238-ea3173ba-4721-4a00-8413-b4a3fb40c6dd.png)




### This was responsibly disclosed to the relevant stakeholders, the vulnerability was patched afterwards. 
