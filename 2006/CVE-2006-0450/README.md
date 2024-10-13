--------------------------------------------------------
[N]eo [S]ecurity [T]eam [NST]® - Advisory #15 - 00/00/06
--------------------------------------------------------
Program:  phpBB 2.0.15

Homepage:  http://www.phpbb.com

Vulnerable Versions: phpBB 2.0.15 & Lower versions

Risk: High Risk!!

Impact: Multiple DoS Vulnerabilities.

---------------------------------------------------------
- Description
---------------------------------------------------------
phpBB is a high powered, fully scalable, and highly customizable
Open Source bulletin board package. phpBB has a user-friendly
interface, simple and straightforward administration panel, and
helpful FAQ. Based on the powerful PHP server language and your
choice of MySQL, MS-SQL, PostgreSQL or Access/ODBC database servers,
phpBB is the ideal free community solution for all web sites.
- Tested
---------------------------------------------------------
localhost & many forums
- Explotation
---------------------------------------------------------
profile.php << By registering as many users as you can.
search.php  << by searching in a way that the db couln't observe it.

CVE: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-0450
