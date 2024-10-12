## Vulnerability Report

CVE Disovered by: Jarod Jaslow (MAWK) 

(DESIGNED TO BE RUN ON KALI LINUX) 

## Notes

Nagios has patched version 2024R1.0.1 in all recent downloads. To determine if a target is vulnerable, ensure they are using an older download of 2024R1.0.1.

The updated script checks to make sure that the target system is vulnerable

OVA NAGIOS USER CREDS: mawk:mawk

DOWNLOAD: https://1drv.ms/u/s!Aj-SNbxrSxWZh51fp476lHxNHGd6jA?e=AX3mJU

![image](https://github.com/user-attachments/assets/de3ac8c7-899a-40f7-92b3-09d7addd2da8)


### Vulnerability Details:

- **Endpoint:** `/nagiosxi//config/monitoringwizard.php` Nagios XI Version 2024R1.0.1 
- **Vulnerability Type:** Authenticated SQL Injection
- **Exploitation Result:** Admin account creation and full remote code execution

### Steps to Reproduce:

1. Create a fresh instance of Nagios XI Version 2024R1.01.
![Pasted image 20240118113507](https://github.com/MAWK0235/NagiosSQLI-CVE-2024-24401/assets/90433993/85fb6873-4066-4927-9f77-96186ed59842)

![Pasted image 20240118113528](https://github.com/MAWK0235/NagiosSQLI-CVE-2024-24401/assets/90433993/5a77e286-5bba-4af4-8c6f-c326011282a2)

![Pasted image 20240118113539](https://github.com/MAWK0235/NagiosSQLI-CVE-2024-24401/assets/90433993/a57ef105-1a10-4d36-a6d4-5e9049e42929)


![Pasted image 20240118113554](https://github.com/MAWK0235/NagiosSQLI-CVE-2024-24401/assets/90433993/22518efd-ceee-48ce-b8ee-7fcb3157e9b8)


3. Create a user with minimum permissions.
![Pasted image 20240118113548](https://github.com/MAWK0235/NagiosSQLI-CVE-2024-24401/assets/90433993/1448fbfb-7c12-4e05-b26b-6baf57edfecf)


4. Execute the provided Python script with the correct arguments:
    ```
    python3 MawkiNagiosXIPOC.py <target IP>
    ```
![image](https://github.com/user-attachments/assets/f2dfccbe-0c43-4ab3-a765-ad715887c43e)


![image](https://github.com/user-attachments/assets/2dc23c9a-b273-4cea-a8a6-f17766ccda38)


### Proof of Concept:

Attached is the Python script demonstrating the vulnerability 

### Recommendation:

To mitigate the risk of SQL injection, it is strongly advised to use parameterized queries or prepared statements when interacting with databases. Parameterized queries ensure that user input is treated as data, not executable code, making it much more difficult for attackers to inject malicious SQL statements.

This is mitigated in recent updates

CVE:

https://cve.mitre.org/cgi-bin/cvename.cgi?name=2024-24401


![image](https://github.com/user-attachments/assets/2e6a9443-a760-4f0c-a87f-4b4921963bc4)


