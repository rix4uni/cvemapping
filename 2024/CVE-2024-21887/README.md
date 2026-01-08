# 🚨 CVE-2024-21887 Exploit Tool 🛠️

A robust tool for detecting and exploiting the CVE-2024-21887 vulnerability in Ivanti Connect and Policy Secure systems.

## 📝 Description

CVE-2024-21887 is a critical command injection vulnerability, allowing authenticated admins to execute arbitrary commands. This tool aids in identifying and interacting with affected systems.

## 🚀 Features

- **Single URL Scan**: Pinpoint focus on a single target.
- **Bulk Scanning**: Analyze multiple URLs from a file.
- **Thread Control**: Customize concurrent scanning with thread options.
- **Output Logging**: Save identified vulnerable URLs to a file.

## 📚 How to Use

1. Install dependencies: `pip install -r requirements.txt`
2. Run the tool:
   - Single URL: `python exploit.py -u <URL>`
   - Bulk scan: `python exploit.py -f <file-path>`
   - With threads: `python exploit.py -f <file-path> -t <number-of-threads>`
   - Save output: `python exploit.py -f <file-path> -o <output-file-path>`

⚠️ **Disclaimer**: This tool is provided for educational and ethical testing purposes only. I am not responsible for any misuse or damage caused by this tool. Always obtain explicit permission before testing systems that you do not own or have explicit authorization to test.
