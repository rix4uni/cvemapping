
# ⚠️ CVE-2024-27954

💀 **Automatic Remote code Execution Exploit Tools | By GhostSec** 💀

---

## 📝 Description

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in WP Automatic Automatic allows Path Traversal, Server Side Request Forgery.This issue affects Automatic: from n/a through 3.92.0.

## ⌛ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/fa-rrel/CVE-2024-27954.git
   cd CVE-2024-27954
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```
---

## 🚀 Usage
- RCE Usage
```bash
python RCE_Exploit.py <target_url> or <File.txt>
```
- Nuclei usage
```bash
nuclei -t POC.yaml --target http://testphp.vulnweb.com/
```

## ☕ Support

If you find this tool useful and want to support the development, consider buying me a coffee:
<a href="https://buymeacoffee.com/ghost_sec" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-white.png" alt="Buy Me a Coffee" width="90"></a>

---

## ⚠️ Disclaimer

This tool is intended for authorized security testing and educational purposes only. Unauthorized use against systems is strictly prohibited.

## 📄 License

This is tools licensed under the MIT License.
