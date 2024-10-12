# CVE-2024-7703
```markdown
# CVE-2024-7703 Exploit: Stored Cross-Site Scripting (XSS) via SVG File Upload in ARMember WordPress Plugin

## Overview

This repository contains a proof-of-concept (PoC) exploit for the vulnerability identified as **CVE-2024-7703**. The vulnerability affects the [ARMember WordPress Plugin](https://wordpress.org/plugins/armember/), specifically in versions up to and including 4.0.37. It allows authenticated attackers with Subscriber-level access or higher to perform Stored Cross-Site Scripting (XSS) attacks by uploading malicious SVG files.

**Summary**:  
The ARMember – Membership Plugin, Content Restriction, Member Levels, User Profile & User signup plugin for WordPress is vulnerable to Stored Cross-Site Scripting via SVG file uploads in all versions up to, and including, 4.0.37 due to insufficient input sanitization and output escaping. This makes it possible for authenticated attackers, with Subscriber-level access and above, to inject arbitrary web scripts in pages that will execute whenever a user accesses the SVG file.

## Details

- **Vulnerability ID**: CVE-2024-7703
- **Plugin**: ARMember - Membership Plugin, Content Restriction, Member Levels, User Profile & User signup
- **Affected Versions**: Up to and including 4.0.37
- **Type**: Stored Cross-Site Scripting (XSS)
- **Severity**: High
- **Access Vector**: Network
- **Privileges Required**: Subscriber-level or higher
- **Impact**: Arbitrary JavaScript code execution, leading to potential session hijacking, data theft, and other malicious actions.

## Requirements

To exploit this vulnerability, you need:

- Access to a WordPress account with at least **Subscriber** permissions.
- The affected version of the ARMember plugin installed on the target WordPress site.
- An HTTP proxy tool such as [Burp Suite](https://portswigger.net/burp).

## Usage

### 1. Clone the Repository

```bash
git clone https://github.com/lfillaz/CVE-2024-7703.git
cd CVE-2024-7703
```


### 2. Understanding the Payload

The payload is a malicious SVG file that contains embedded JavaScript. When this SVG file is uploaded to a vulnerable WordPress site, the script will execute when the file is viewed.

Here’s an example of the payload:

```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>alert('XSS Attack!');</script>
</svg>
```

You can modify the JavaScript inside the `<script>` tags to perform different actions, such as stealing cookies, redirecting users, or injecting additional scripts.

### 3. Exploitation Steps

1. **Login to WordPress:**  
   Use your Subscriber-level (or higher) credentials to log in to the target WordPress site.

2. **Capture the File Upload Request:**  
   - Use Burp Suite or any similar tool to capture the HTTP request when you attempt to upload a file.
   - Replace the file content with the payload provided in this repository.

3. **Send the Modified Request:**  
   - Forward the modified request with the malicious SVG file to the server.
   - If the upload is successful, the SVG file will now be stored on the server.

4. **Trigger the Payload:**  
   - Navigate to the page where the SVG is rendered.
   - The JavaScript code inside the SVG file will execute in the context of the user viewing the page.

### 4. Mitigation

To mitigate this vulnerability, users are strongly advised to:

- Update the ARMember plugin to the latest version as soon as a patch is released.
- Restrict file uploads to trusted users and limit allowed file types.
- Implement a Web Application Firewall (WAF) to detect and block malicious file uploads.

## Disclaimer

This exploit is intended for educational and testing purposes only. Unauthorized use of this code against systems that you do not have explicit permission to test is illegal and unethical. The author is not responsible for any misuse of this code.


- [WordPress ARMember Plugin](https://wordpress.org/plugins/armember/)
- [CVE-2024-7703 on NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-7703)
- [Burp Suite](https://portswigger.net/burp)

```
I hope this helped you enjoy 
