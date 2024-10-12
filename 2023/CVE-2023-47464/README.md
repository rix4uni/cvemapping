# GL-AX1800 Router Security Assessment Report

## Overview

This report outlines the findings of a comprehensive security assessment conducted on the GL-AX1800 router manufactured by GL.iNet. The assessment aimed to identify potential vulnerabilities and weaknesses in the device's security measures. During the evaluation, several critical security issues were discovered, including Cross-Site Request Forgery (CSRF), insecure file uploads, path traversal, file overwrite leading to Remote Code Execution (RCE), and unrestricted file access download.

## Vulnerabilities

### Cross-Site Request Forgery (CSRF)

The GL-AX1800 router is susceptible to CSRF attacks, which allow unauthorized parties to execute unwanted actions on behalf of authenticated users. By crafting malicious requests and tricking users into visiting specially crafted web pages, attackers can manipulate router settings, potentially leading to unauthorized access or control over the device.

### Insecure File Uploads

The assessment revealed that the GL-AX1800 router permits insecure file uploads without adequate validation and authorization checks. This vulnerability allows attackers to upload malicious files, leading to potential remote code execution or unauthorized access to sensitive system resources.

### Path Traversal

The GL-AX1800 router suffers from a path traversal vulnerability, which enables attackers to navigate outside of the intended directory structure. This flaw can be exploited to access restricted files or execute arbitrary code, posing a significant threat to the integrity and confidentiality of the device and its data.

### File Overwrite -> Remote Code Execution (RCE)

Through the combination of insecure file uploads and file overwrite vulnerability, an attacker can overwrite critical system files with malicious content. This scenario may lead to remote code execution, enabling unauthorized control and manipulation of the router's functionalities.

### Unrestricted File Access Download

The assessment uncovered a flaw that allows attackers to download sensitive files or confidential data from the GL-AX1800 router without proper authentication or authorization. This issue poses a severe risk of data exfiltration and unauthorized access to the device's configuration files and other critical information.

## Proof of Concept (PoC)

A Python script has been developed to demonstrate the exploitation of the CVE-2023-47464 vulnerability in the GL-AX1800 router. The script provides the following features:

- Command-line options:
  - `-h`: Displays help information.
  - `-ip`: Retrieves the GL-AX1800 instance IP address.
  - `--username`: Retrieves the username placeholder.
  - `--password`: Retrieves the password placeholder.
  - `--check`: Checks for the existence of the exploit.
- Exploit: Sends a request to the `/upload` endpoint with a crafted payload, exploiting the vulnerability to upload a file to the device.

For detailed usage instructions and further information, refer to the script documentation and comments.

**Note:** This PoC script is for educational and research purposes only. Use it responsibly and only on devices you are authorized to test. Unauthorized access to computer systems and networks is illegal and unethical.

---
*Disclaimer: This report is for informational purposes only. The vulnerabilities identified in this report may have been addressed by the vendor through patches or updates. It is recommended to keep the device firmware up to date and follow best security practices to mitigate the risks associated with these vulnerabilities.*
