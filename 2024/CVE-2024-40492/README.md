# CVE-2024-40492: Stored XSS to ATO

## Description
Stored Cross-Site Scripting (XSS) is a type of security vulnerability typically found in web applications. It occurs when an attacker is able to inject malicious scripts into a web application, and those scripts are stored on the server. When other users access the data containing the malicious script, the script is executed in their browsers.

## Steps to Reproduce
1. Go to https://app.heartbeat.chat/
2. Create an account with the following details:
   - **First name:** 
     ```html
     giongfnef"><h1>test</h1>"><img src=1 onerror=alert(document.cookie)>
     ```
   - **Last name:** 
     ```html
     giongfnef"><img src=1 onerror=alert(document.cookie)>
     ```
3. Go to "Threads" then search for the first name `giongfnef` -> XSS is triggered -> this is stored XSS which can lead to Account Take Over

## POC
[Link POC  to reproduce the exploit](https://youtu.be/iLYpPiZud8w)

## Impact
After triggering the XSS, I can proceed with an Account Take Over. Since this is a stored XSS, any user who views the user section or searches for the user `giongfnef` will trigger the XSS and have their session stolen.

## Mitigation
To prevent stored XSS vulnerabilities, follow these best practices:
- **Input Validation:** Validate and sanitize all user inputs on the server-side.
- **Output Encoding:** Encode data before displaying it in the browser to prevent execution of injected scripts.
- **Use Security Libraries:** Use libraries and frameworks that automatically handle input sanitization and output encoding.
- **Content Security Policy (CSP):** Implement CSP headers to restrict the sources from which scripts can be loaded.

Thanks for reading, have a nice day!
