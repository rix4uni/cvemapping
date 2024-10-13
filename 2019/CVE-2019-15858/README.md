# CVE-2019-15858
**Unauthenticated Remote Code Execution at Woody Ad Snippets (PoC)**

The vulnerabilities discovered by **nintechnet** and exploit released by **GeneralEG** & **X-Vector**

An unauthenticated options import vulnerability combined with a stored XSS vulnerability can lead to remote code execution in the WordPress Woody Ad Snippets (90,000+ active installations).
Woody Ad Snippets is a plugin that allows administrators to insert any code, text, or ads by conditions in their blog: JS, CSS, HTML and even PHP code. It was prone in version 2.2.4 and below to two vulnerabilities that, when unintentionally triggered by the administrator in the back-end section of WordPress, would allow an attacker to run any PHP code in order to compromise the website and its database.

# Usage:
```
usage: python exploit.py sites.txt payload.json
```

[![Proof of Concept Video](https://img.youtube.com/vi/n3zDjJ-xJ_8/0.jpg)](https://www.youtube.com/watch?v=n3zDjJ-xJ_8)

# References:
* https://blog.nintechnet.com/multiple-vulnerabilities-in-wordpress-woody-ad-snippets-plugin-lead-to-remote-code-execution/
* https://www.cvedetails.com/cve/CVE-2019-15858/
* https://wordpress.org/plugins/insert-php/
