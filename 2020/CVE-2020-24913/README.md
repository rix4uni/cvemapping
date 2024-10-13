# CVE-2020-24913-PoC
A Poc for CVE-2020-24913, a SQL injection vulnerability in qcubed (all versions including 3.1.1) in profile.php via the strQuery parameter allows an unauthenticated attacker to access the database by injecting SQL code via a crafted POST request. This PoC is performed using a MySQL database. We were not able to use a stacked-queries-payload (as it can be done with postgres) and we had to exploit this vulnerability with a timebased approach.
# Payloads
In the "strProfileData" parameter, we use the following payload (unencoded):
a:1:{i:0;a:3:{s:12:"objBacktrace";a:1:{s:4:"args";a:1:{i:0;s:3:"pwn";}}s:8:"strQuery";s:38:"(SELECT * FROM (SELECT(SLEEP(10)))CP);";s:11:"dblTimeInfo";s:1:"1";}}
# PoC
The vulnerable parameter is "strProfileData". A successful request to send to the server looks like this. The PHP serialized array that is sent in this parameter must be base64 encoded.
![image](https://github.com/agarma/CVE-2020-24913-PoC/assets/170352821/f20547e2-a631-4337-8458-606e7d11c50b)
For the following images, the strProfileData parameter has been base64 decoded so that the reader can see it more clearly, but as mentioned above it must be sent base64 encoded. 
The following request contains a query that makes the server sleep 10 seconds. We are going to exploit the SQL injection vulnerability by sending a SQL query to the database which forces it to wait a specified amount of time (in seconds) before responding.
![image](https://github.com/agarma/CVE-2020-24913-PoC/assets/170352821/2c3014b9-bd36-4e7e-a9eb-9ff41f9b0057)
And to get the data from the database, we will are going to use an IF structure that makes the database sleep more or less time depending on whether the condition is true or not.
![image](https://github.com/agarma/CVE-2020-24913-PoC/assets/170352821/b979ba04-5c08-4215-bd25-b906e2c9236c)
In the following images we obtain the first characters of the database version (8.0.XX)
We use the SQL query "SLEEP(5-(IF(SUBSTRING(@@version,X,1)='Y',2,5)))" which makes the database sleep (5-2)=3 seconds if the condition is true, or which makes the database sleep (5-5)=0 seconds if the condition is false. The condition is that the character of the database version in the position X is equal to character Y.
![image](https://github.com/agarma/CVE-2020-24913-PoC/assets/170352821/95c4aae2-d2bf-4822-9117-652c7ea070d2)
![image](https://github.com/agarma/CVE-2020-24913-PoC/assets/170352821/792b3a8e-8d98-46b0-a688-fb2e288424c8)
