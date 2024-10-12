# CVE-2024-2997
# CVE-2024-2997 URL Vulnerability Scanner
![image](https://github.com/user-attachments/assets/fedbcd45-0f14-4938-b756-46bdaeb9b685)
![image](https://github.com/user-attachments/assets/28d9ee68-c2b6-43e7-adee-38c0fbddf24f)
```markdown
## Features

- Generates a wide range of URLs based on a base URL.
- Scans URLs for a specific command injection vulnerability.
- Uses multithreading for faster scanning.
- Displays results in a color-coded format.
- Saves vulnerable URLs to a file for future reference.
- Allows resuming scans from a previous session.

## Requirements

- Python 3.x
- `requests`
- `colorama`

You can install the required libraries using pip:

```bash
pip install requests colorama
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/lfillaz/CVE-2024-2997.git
cd CVE-2024-2997
```

2. Run the script:

```bash
python CVE-2024-2997.py
```

3. Follow the on-screen instructions to input the base URL and start the scan.

## How It Works
1. The script prints an ASCII art banner and starts the scanning process.
2. It checks if a previous session file `scope.txt` exists:
    - If it exists, the user can choose to continue scanning the URLs from the previous session or start a new session.
    - If it doesn't exist, a new session is started.
3. The user inputs the base URL.
4. The script generates a wide range of URLs based on the base URL.
5. The user is prompted to start the scan.
6. The script scans each URL for the command injection vulnerability, displaying the results in a color-coded format:
    - Vulnerable URLs are displayed in red.
    - Safe URLs are displayed in green.
7. Results are saved to `sus.txt`.

## Example

```plaintext
  _____  _   __   ____        ___   ___    ___   ____        ___   ___   ___  ____   ____
 / ___/ | | / /  / __/ ____  |_  | / _ \  |_  | / / / ____  |_  | / _ \ / _ \/_  /  |_  /
/ /__   | |/ /  / _/  /___/ / __/ / // / / __/ /_  _//___/ / __/  \_, / \_, / / /  _/_ <
\___/   |___/  /___/       /____/ \___/ /____/  /_/       /____/ /___/ /___/ /_/  /____/  
          by GhostByte

Script is running!
Scan started at 2024-08-03 14:00:00
A previous session file 'scope.txt' exists.
Do you want to scan the existing URLs (y) or create a new session (n)? (y/n): y
Scanning existing URLs...
Starting scan for http://example.com/path
[SAFE] http://example.com/path is not vulnerable
...
Scan completed.
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Disclaimer

This tool is intended for educational purposes only. Use it responsibly and only on web applications you own or have permission to test. The author is not responsible for any misuse of this tool.

```
https://t.me/laz_dev #2024/7/3
