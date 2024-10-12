# CVE-2023-40297
 Stakater Forecastle => v1.0.144 allows directory traversal in the website component
 
[Vulnerability Type] Directory Traversal

[Vendor of Product] Stakater

[Affected Product Code Base] Forecastle => v1.0.144

[Affected Component] Affected component(s): URL - https://www.example.com/%5C../etc/passwd

[Attack Type] Local

[Impact Escalation of Privileges] true

[Impact Information Disclosure] true

[Attack Vectors]

Attack vector(s):
https://<domain/ip>/%5C../etc/passwd

An attacker can exploit the directory traversal vulnerability by manipulating the URL to traverse outside the intended web directory. By appending "%5C../etc/passwd" to the URL, an unauthorized user can access the sensitive system file "/etc/passwd" containing user account information. This allows the attacker to obtain privileged information about system users, potentially facilitating further attacks.

POC:<br>
![image](https://github.com/user-attachments/assets/6787451c-aede-4c52-b5a2-4d7329cfe2ec)


[Reference]
https://github.com/stakater/Forecastle/releases

[Discoverer]
Sahar Shlichove
