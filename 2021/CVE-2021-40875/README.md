# TestRail-files.md5-IAC-scanner
Improper Access Control in Gurock TestRail versions < 7.2.0.3014 resulted in sensitive information exposure. A threat actor can access the /files.md5 file on the client side of a Gurock TestRail application, disclosing a full list of application files and the corresponding file paths. The corresponding file paths can be tested, and in some cases, result in the disclosure of hardcoded credentials, API keys, or other sensitive data.

Source: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-40875

# Summary
This script was written to be able to quickly identify which files on a CVE-2021-40875 vulnerable TestRail server can be accessed by looking at the returned text, by identifying the status code is not 500, and then it identifies any interesting keywords found in the file.

Keywords to look for can be modified in line 4 of scanner.py.

# Usage
Python
```
git clone https://github.com/Lul/TestRail-files.md5-IAC-scanner.git
cd ./TestRail-files.md5-IAC-scanner
python3 scanner.py
 -> Input server in http:\\ or https:\\ format
 ```
 
 The script will print out the server/file location, status code (if not 500), and any interesting keywords found.
