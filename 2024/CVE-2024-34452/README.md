CVE-2024-34452 - Cross-Site Scripting (XSS) Vulnerability in CMSimple_XH
---
Overview

A cross-site scripting (XSS) vulnerability has been identified in CMSimple_XH version 1.7.6. This vulnerability allows authorized users to upload SVG files containing malicious JavaScript code. The issue stems from inadequate validation and sanitization of uploaded SVG files within the file upload functionality of the application.

Vulnerability Details

- CVE Identifier: CVE-2024-34452
- Severity: Medium
- Affected Version: CMSimple_XH 1.7.6

Description

The vulnerability exists due to the application's failure to properly validate and sanitize SVG files uploaded by users. An attacker can exploit this flaw by uploading a specially crafted SVG file containing malicious JavaScript code. When the uploaded SVG file is accessed by other users, the injected JavaScript code executes within their browsers in the context of the CMSimple_XH application. This can lead to various XSS attacks.

Impact

Successful exploitation of this vulnerability could enable an attacker to:

- Steal session cookies
- Compromise user accounts
- Perform unauthorized actions on behalf of legitimate users

Proof of Concept

An example of a malicious SVG code that triggers an alert with the document's cookies:

---
```xml
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
  <polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400"/>
  <script type="text/javascript">
    alert(document.cookie);
  </script>
</svg>
```
---
Steps to Reproduce

1. Log in to the CMSimple_XH application as an authorized user.
2. Navigate to the file upload functionality.
3. Upload the malicious SVG file (xss.svg) provided in the Proof of Concept section.
4. Access the uploaded SVG file within the application.
5. Observe the execution of the JavaScript code and the alert displaying the document's cookies.

Screenshots
![xss triaged](https://github.com/surajhacx/CVE-2024-34452/assets/158517938/56a98fcd-be2a-4558-8376-8f3792f83d13)

Acknowledgements:
This vulnerability was discovered and reported by Suraj Theekshana.





