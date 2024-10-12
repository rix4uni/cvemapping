# 🚀 HashForm Exploit Script

This script demonstrates the exploitation of CVE-2024-5084, a vulnerability in the Hash Form plugin for WordPress, which allows unauthenticated arbitrary file upload leading to remote code execution.

## 📖 Vulnerability Details

- **Name**: CVE-2024-5084
- **Description**: Unauthenticated Arbitrary File Upload to Remote Code Execution.
- **Affected Plugin**: Hash Form – Drag & Drop Form Builder <= 1.1.0
- **Source**: [Wordfence - Vulnerability Details](https://www.wordfence.com/threat-intel/vulnerabilities/wordpress-plugins/hash-form/hash-form-drag-drop-form-builder-110-unauthenticated-arbitrary-file-upload-to-remote-code-execution)

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Chocapikk/CVE-2024-5084.git
   cd CVE-2024-5084
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Run the script:
   ```bash
   python exploit.py --url "http://target-site.com"
   ```

   Replace `http://target-site.com` with the base URL of the WordPress site you want to test.

2. If the upload is successful, you will enter an interactive shell to execute commands on the server.

## 🔍 Dorks

- **ZoomEye**: `banner:"var hashform_vars"`

## ⚠️ Disclaimer

**Disclaimer**: This script is intended for educational purposes only. Unauthorized use of this script on systems you do not own or do not have explicit permission to test is illegal and unethical. The author is not responsible for any misuse of this script.