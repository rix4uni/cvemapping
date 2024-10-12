# CVE-2024-9166 Vulnerability Scanner
A Python-based tool to scan websites for the CVE-2024-9166 vulnerability, **which is one of the most recent ones** (at the moment of publishing this repository.). It checks for vulnerable patterns, tests the vulnerability to confirm it, and logs results to a file.

**I'm not responsible in any way of the misuse of this tool. This tool was made with the intention of being used for ethical hacking, doing penetration testing (and every type of hacking) without consent is illegal and can have serious consequences!**

## Installation
To install the tool you can just copy this Github repository with this single command:
```bash
git clone https://github.com/Andrysqui/CVE-2024-9166
```

### Requirements
  * Python 3.7+
  * Install Python dependencies via `pip`:
  ```bash
  pip install requests beautifulsoup4 argparse
  ```

## Usage
### Basic Usage:
  1. **Single URL Scan:**
  ```bash
    python3 CVE-2024-9166.py --url https://example.com
  ```
  2. **Scan Multiple URLs from a File and Logging the Results:**
  ```bash
    python3 CVE-2024-9166.py --file urls.txt --logfile output.log
  ```
  3. **Custom Headers**
  ```bash
    python3 CVE-2024-9166.py --url https://example.com --headers '{"User-Agent": "Custom-Agent", "Bug-Bounty: True", "Pen-Testing: True"}'
  ```

### Command-Line Arguments:
  * `-h` or `--help`: Shows a help message explaining each one of the arguments below.
  * `--url` or `-u`: Specify a single URL to scan (mutually exclusive with `-f` or `--file`).
  * `--file` or `-f`: Path with a file with URLs to scan (one per line, mutually exclusive with `-u` or `--url`).
  * `--logfile` or `-l`: Path to log results (default: `scan_log.txt`).
  * `--headers`: Custom headers in JSON format (e.g., `'{"User-Agent": "Custom-Agent"}'`).
  * `--threads`: Number of threads for scanning multiple URLs (default: 5).
  * `--exploit-command`: Command used to test the vulnerability (default: `id`).
  * `--vulnerable-content`: Pattern to search for inside responses to confirm a vulnerability when using custom command (default: `uid=`).
