# CVE-2024-41662
Markdown XSS leads to RCE in VNote version &lt;=3.18.1

**Severity :** **High** (**8.6**)

**CVSS score :** `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` 

## Summary :

A **Cross-Site Scripting (XSS)** vulnerability was identified in the Markdown rendering functionality of the VNote note-taking application. This vulnerability allows the injection and execution of arbitrary JavaScript code, potentially leading to **Remote Code Execution (RCE)**.

## Steps to Reproduce :

1. Create a note in Vnote.
2. Enter the following JS payload in the app,
   
```html
<img src="" onerror="alert('XSS') alt="alt text">
```
3. Press **CTRL+T** to render the markdown content.
4. Observe the JavaScript payload executing an alert popup.

![image](https://github.com/user-attachments/assets/8124c2a0-e5df-461d-af11-991d918cbb87)

There is no whitelisting or output encoding performed for the given payload, resulting in an XSS vulnerability.

> NOTE: The application properly validates some JavaScript payloads by performing output encoding in the app. However, it fails to validate in certain cases.

![image](https://github.com/user-attachments/assets/fea2b50d-0cd1-441d-8d76-6478b7c26c86)

![image](https://github.com/user-attachments/assets/e836ab2a-ca9c-4e45-8ab6-013fb37d58fb)

5. Further an attacker can achieve **Remote Code execution** using the following payload.

```html
<iframe src="../../../../../../../../Windows/System32/cmd.exe"  />
```
![image](https://github.com/user-attachments/assets/07469a14-0bad-494d-9033-55a8cfbffc93)


## Affected Version Details :

- <=3.18.1

## Impact :

This vulnerability can be exploited by an attacker to gain unauthorized access to the system, execute arbitrary commands, and potentially take control of the affected machine. This could lead to system compromise and other severe security incidents.

## Mitigation :

- Implement rigorous input sanitization for all Markdown content.
- Utilize a secure Markdown parser that appropriately escapes or strips potentially dangerous content.

## References :

- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-41662
- https://nvd.nist.gov/vuln/detail/CVE-2024-41662
- https://github.com/sh3bu/CVE-2024-41662
