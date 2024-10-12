# CVE-2024-4484

---

### Cross-Site Scripting (XSS) Vulnerability Detector

This script uses `HTTParty` to detect stored cross-site scripting (XSS) vulnerabilities in WordPress sites using the `xai_username` parameter. It sends a payload to the specified URL and checks if the payload is reflected in the response, indicating a vulnerability.

#### Features
- Sends a POST request with a potential XSS payload.
- Checks if the response contains the payload, indicating a stored XSS vulnerability.
- Supports authentication by including cookies in the request.

---
