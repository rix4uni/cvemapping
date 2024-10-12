## AppCheck - arbitrary file write to lpe

![image](https://github.com/Team-Byerus/CVE-2023-51000/assets/99308681/62b1a814-b04c-43ba-99dc-0d262bdc437c)


https://github.com/Team-Byerus/CVE-2023-51000/assets/99308681/35627512-3eeb-4450-ab7f-302b08eeaef9


Vulnerabilities occur in all user environments that attempt to install the latest version of AppCheck.
In the process of running the installation anti-virus process level at "High" or higher, folders that can be accessed by regular users are read/written, and a symbolic vulnerability (lace condition) is used to arbitrarily access folders that require the same permissions as the System32 folder with regular user permissions. File writing is possible.
So the attacker indiscriminately distributes it in advance, waits for the user to install AppCheck, and then the vulnerability is triggered upon installation.

## Credit Information

Team Byerus (HeeChan Kim, Jinyoung Kim, MinkUk Kim, Seoungjin, Oh, Sangsoo Jeong)
