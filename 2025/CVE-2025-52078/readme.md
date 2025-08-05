
# 🚨 CVE-2025-52078 - Unauthenticated Arbitrary File Upload - Writebot SaaS React Template

This repository contains a proof-of-concept exploit for an **Unauthenticated Arbitrary File Upload** vulnerability found in the **Writebot – AI Content Generator SaaS React Template**.

🧠 **Product Page:**  
[ThemeForest – Writebot](https://themeforest.net/item/writebot-ai-content-generator-saas-react-template/53331158?s_rank=9)

---

## 🆔 Vulnerability Metadata

- **CWE-ID:** [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- **Severity:** Critical
- **Exploit Type:** Remote Code Execution (via File Upload)
- **Authentication Required:** ❌ No
- **User Interaction Required:** ❌ No
- **CVE:** CVE-2025-52078
- **Public Exploit Available:** ✅ Yes
- **Patched:** ❌ Not confirmed
- **Researcher:** Yucaerin

---

## 🧨 Vulnerability Summary

The template exposes a file upload endpoint at:

```
POST /file-upload
```

Due to the lack of:
- MIME/type validation
- Extension checks
- Authentication or session validation

An attacker can upload a **malicious PHP file disguised as an image**, and execute arbitrary commands once it's written to a publicly accessible directory.

---

## ✅ Features

- 🔁 Mass exploitation (multi-threaded)
- 🔐 Auto CSRF token extraction from `<meta name="csrf-token">`
- 🍪 Session-based cookie handling
- 🐚 Uploads `bq.php` shell disguised as `image/jpeg`
- 📁 Saves valid shell URLs to `result.txt`

---

## ⚙️ Requirements

- Python 3.x
- Modules:
  - `requests`
  - `beautifulsoup4`

Install modules:

```bash
pip install requests beautifulsoup4
```

---

## 📁 Structure

```
writebot.py         # Main exploit script
list.txt            # Domains
bq.php              # Payload disguised as JPEG
result.txt          # Shell URLs on success
```

---

## 🚀 Usage

1. Put target domains in `list.txt`:
    ```
    test-web-dummy-site.ai
    vulnerable.site
    ```

2. Ensure `bq.php` contains this format:
    ```php
    ÿØÿà

    <?php
    // Your code
    ?>
    ```

3. Run exploit:
    ```bash
    python3 mass_uploader.py
    ```

4. Shell URLs saved to `result.txt`.

---

## 🔒 Recommendations for Developers

To mitigate:

- ✅ Require authentication for uploads
- ✅ Sanitize and validate MIME + file extensions
- ✅ Store uploaded files outside webroot
- ✅ Randomize filenames and restrict access

---

## ⚠️ Legal Disclaimer

This project is for **educational and authorized testing** purposes only.  
Unauthorized use against websites you do not own or have permission to test is illegal and unethical.
