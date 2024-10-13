# CVE-2015-2166 - Directory Traversal Vulnerability in Ericsson Drutt Mobile Service Delivery Platform (MSDP)

CVE-2015-2166 is a directory traversal vulnerability that affects the Instance Monitor in Ericsson Drutt Mobile Service Delivery Platform (MSDP) versions 4, 5, and 6. The vulnerability allows remote attackers to read arbitrary files on the affected system by exploiting a "..%2f" (dot dot encoded slash) in the default URI.

# Vulnerable Versions

    Ericsson Drutt Mobile Service Delivery Platform (MSDP) version 4
    Ericsson Drutt Mobile Service Delivery Platform (MSDP) version 5
    Ericsson Drutt Mobile Service Delivery Platform (MSDP) version 6

# Impact and Severity

The presence of this vulnerability poses a severe security risk as it enables unauthorized access to sensitive files on the Ericsson Drutt MSDP system. Exploitation of this flaw can result in the exposure of critical information or configuration files, potentially leading to further compromise of the system or unauthorized access to sensitive data.

# Mitigation

To address the vulnerability and prevent potential exploitation, users of the Ericsson Drutt MSDP are strongly advised to take the following actions:

    Update to a Fixed Version: Ericsson should release a security patch that addresses the directory traversal vulnerability. Users should promptly update to the latest version of the MSDP that includes the fix.
    Input Validation and Sanitization: Implement stringent input validation and sanitization mechanisms within the Instance Monitor to filter out or escape malicious characters, including "../" sequences and encoded slashes (%2f).
    Access Controls: Review and improve access controls for the affected application, ensuring that only authorized users have access to sensitive functionalities and files.
    Web Application Firewall (WAF): Consider deploying a WAF in front of the Ericsson Drutt MSDP to filter and block malicious requests, including those attempting directory traversal attacks.
    Security Audits: Conduct regular security audits of the system to identify and address potential vulnerabilities promptly.

# How the Vulnerability Works

The vulnerability arises due to insufficient input validation in the Instance Monitor of the Ericsson Drutt MSDP. When processing user-supplied input in the default URI, the application fails to properly validate and sanitize the input. As a result, an attacker can craft malicious HTTP requests containing "..%2f" sequences, which get decoded as "../" by the server. This allows the attacker to navigate to directories outside of the intended path, granting access to arbitrary files on the filesystem.

By exploiting this flaw, an attacker can read sensitive files, such as configuration files or other critical data, potentially facilitating further attacks or unauthorized actions on the system.

# Proof of Concept (PoC)

As an illustration, consider the following example of a crafted HTTP request:

GET /InstanceMonitor/..%2f..%2f..%2fetc/passwd HTTP/1.1

Host: vulnerable-msdp.com

In this PoC, the attacker manipulates the URI by using the "%2f" encoded slash to traverse multiple directories, eventually reaching the "/etc/passwd" file. If the vulnerability is present and successfully exploited, the contents of the passwd file would be returned in the HTTP response, potentially revealing sensitive information.

Note: The provided PoC is for demonstration purposes only and should not be used against any system without explicit authorization.

# Disclaimer

This advisory describes a known security vulnerability in the specified versions of Ericsson Drutt Mobile Service Delivery Platform (MSDP). It is crucial to adhere to responsible disclosure practices and follow the guidelines set forth by Ericsson. The information provided in this advisory is for educational purposes only.
