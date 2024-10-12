# CVE-2024-44542

Description: todesk v1.1 was discovered to contain a SQL injection vulnerability via the title parameter at /todesk.com/news.html.

Vulnerability Type: SQL Injection

Vendor of Product: todesk

Affected Product Version: todesk - v1.1

Affected Component: todesk.com, news.html

Attack Type: Remote

Impact Information Disclosure: True

Attack Vectors: By constructing a specific URL request, an attacker can exploit the SQL injection vulnerability, for example: accessing https://todesk.com/news.html?tag_id=&title=1' AND (SELECT 6268 FROM (SELECT(SLEEP(10)))ghXo) AND 'IKlK'='IKlK.

Date Published: 2024/09/14
