# 🕵️ Vulnerability Scanner 🛡️

This Python script helps you scan websites for specific vulnerabilities and fetches information regarding authorized users.

## 📌 Features

- Scans URLs for known vulnerabilities (CVE-2023-35082, CVE-2023-35078).
- Retrieves and prints the first 10 email addresses, display names, last login IPs, and roles.
- Supports mass scanning through a file containing a list of URLs.
- Can output results to a file.

## 🔧 How to Use

1. Clone the repository or download the script.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script with the desired options:

   - Single URL:

     ```bash
     python exploit.py -u <URL> --verbose
     ```

   - Multiple URLs from a file:

     ```bash
     python exploit.py -f <file.txt> --verbose
     ```

   - Save output to a file:

     ```bash
     python exploit.py -u <URL> -o <output_file.txt>
     ```

## 🎓 Parameters

- `-u, --url`: Base URL for the request.
- `-f, --file`: File containing a list of URLs for mass scanning.
- `-o, --output`: Output file to save vulnerable URLs and first 5 emails.
- `--verbose`: Verbose mode (optional).

## 🛑 Disclaimer

Please use this script responsibly and only on websites that you have the proper authorization to scan. Unauthorized scanning may lead to legal issues.


