# CVE-2024-6043
```markdown
# CVE-2024-6043 CVE-2024-6043

## Overview

This Python tool exploits the CVE-2024-6043 vulnerability, which affects the SourceCodester Best House Rental Management System 1.0. The vulnerability allows remote attackers to perform SQL Injection via the `admin_class.php` file, specifically targeting the `username` parameter in the login function. This tool automates the process of detecting the vulnerable endpoint and injecting a payload to bypass authentication.

## Features

- **Automated Path Detection**: The tool checks if the vulnerable `admin_class.php` file exists on the target server.
- **SQL Injection Payload**: If the path is found, the tool attempts to inject a SQL payload that bypasses the admin login.
- **Success Check**: The tool verifies if the SQL Injection was successful by searching for common indicators of successful login.
- **Custom User-Agent**: The tool sends requests with a custom User-Agent to mimic legitimate browser traffic.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lfillaz/CVE-2024-6043.git
   cd CVE-2024-6043
   ```


## Usage

1. **Run the tool:**
   ```bash
   python CVE-2024-6043.py
   ```

2. **Enter the target URL:**

3. 
   When prompted, enter the URL of the target site (e.g., `http://target-site.com`).

4. **Injection Process:**
   - The tool will check if the `admin_class.php` path exists on the target server.
   - If found, you will be prompted to proceed with the SQL Injection.
   - The tool will then attempt to inject the payload and provide feedback on the success or failure of the attack.

## Example
```bash
 ██████╗██╗   ██╗███████╗      ██████╗  ██████╗ ██████╗ ██╗  ██╗       ██████╗  ██████╗ ██╗  ██╗██████╗ 
██╔════╝██║   ██║██╔════╝      ╚════██╗██╔═████╗╚════██╗██║  ██║      ██╔════╝ ██╔═████╗██║  ██║╚════██╗
██║     ██║   ██║█████╗  █████╗ █████╔╝██║██╔██║ █████╔╝███████║█████╗███████╗ ██║██╔██║███████║ █████╔╝
██║     ╚██╗ ██╔╝██╔══╝  ╚════╝██╔═══╝ ████╔╝██║██╔═══╝ ╚════██║╚════╝██╔═══██╗████╔╝██║╚════██║ ╚═══██╗
╚██████╗ ╚████╔╝ ███████╗      ███████╗╚██████╔╝███████╗     ██║      ╚██████╔╝╚██████╔╝     ██║██████╔╝
 ╚═════╝  ╚═══╝  ╚══════╝      ╚══════╝ ╚═════╝ ╚══════╝     ╚═╝       ╚═════╝  ╚═════╝      ╚═╝╚═════╝ 
                                                                                                        
          BY @GhostByte discord.gg/byt
$ python CVE-2024-6043.py
Enter the target site (e.g., http://target-site.com): http://example.com
Checking if http://example.com/admin_class.php exists...
The path exists.
Do you want to inject the payload? (Y/N): y
Injecting... Done.
SQL Injection successful! Admin login bypassed.
```

## Disclaimer

This tool is intended for educational purposes only. Use it responsibly and only on systems where you have explicit permission to test. Misuse of this tool could lead to legal consequences.
## Author

- **GhostByte** - [Discord](https://discord.gg/byt)
```
have fun
