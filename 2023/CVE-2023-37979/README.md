# CVE-2023-37979 Exploit

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Nuclei](https://img.shields.io/badge/Nuclei-template-yellow.svg)

| CVE ID        | CVSS Score   | Discovered   | Affected Plugin  | Vendor         | Vulnerability Type |
|--------------|-------------|-------------|-----------------|---------------|--------------------|
| CVE-2023-37979 | ![Medium](https://img.shields.io/badge/5.0-Medium-orange) | 27/07/2023 | WordPress Plugin | Ninja-forms | Reflected XSS |

## 🐍 Python Script
This Python script exploits the reflected Cross-Site Scripting (XSS) vulnerability CVE-2023-37979 found in the Ninja-forms WordPress plugin.  
This vulnerability allows attackers to inject arbitrary scripts (e.g., redirects, phishing payloads) which execute when users interact with certain pages.  
🔹 **Fixed in version 3.6.26.**  

## 🛠 Nuclei Template
I have also created a **Nuclei template** to detect vulnerable versions of the plugin (`<= 3.6.25`).  
While the Python script provides **exploit verification**, the Nuclei template is ideal for **bulk scanning** and **automated detection**.

---

## 🚀 Usage
```bash
python3 CVE-2023-37979.py [OPTIONS] [TARGET]

OPTIONS:
        --exploit    Open a browser and execute the vulnerability.

TARGET:
        A URL starting with 'http://' or 'https://'

Examples:
    python3 CVE-2023-37979.py https://vulnsite.com
    python3 CVE-2023-37979.py --exploit https://vulnsite.com
```

## 🔍 How It Works
1️⃣ The script checks if Ninja-forms is installed and determines its version.

2️⃣ If vulnerable (<= 3.6.25), it generates a PoC HTML file containing the exploit payload.

3️⃣ If the --exploit flag is used, the PoC file automatically opens in the browser for testing.

> **⚠️ Disclaimer**
> This script is intended for educational and ethical security testing purposes only.
> Unauthorized testing is illegal. The author assumes no responsibility for misuse.

**📜 References**
[🔗 Patchstack - Ninja Forms XSS Advisory](https://patchstack.com/articles/multiple-high-severity-vulnerabilities-in-ninja-forms-plugin?_s_id=cve)
[🔗 Exploit-DB](https://www.exploit-db.com/exploits/51644)
