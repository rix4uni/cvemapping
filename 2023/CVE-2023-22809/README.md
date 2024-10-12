# CVE-2023-22809 Exploiter Scripts

Disclaimer
This script is provided for educational purposes only. The author is not responsible for any misuse or unintended consequences resulting from its use. Always follow ethical guidelines and obtain proper authorization before testing any security tools or exploits.

## Description

This Python and Bash scripts are designed to exploit the CVE-2023-22809 vulnerability in `sudo` versions 1.8.0 through 1.9.12p1. This vulnerability allows a local attacker to escalate their privileges by exploiting improper handling of `sudoedit` or `sudo -e` commands.

## Requirements

- Python 3.x | Bash
- `sudo` version 1.8.0 through 1.9.12p1 installed on the target machine 
- Access to the `sudo` command with potential `sudoedit` or `sudo -e` capabilities

## Usage

### Basic Usage
The basic usage of this script:
- To execute the script and exploit CVE:
```python
python exploit.py
```
Or
```bash
bash exploit.sh
```

### Options
- To see information about the vulnerability:
```python
python exploit.py -i
```
Or
```bash
bash exploit.sh -i
```
- To see pre requirements for the vulnerability:
```python
python exploit.py -r
```
Or
```bash
bash exploit.sh -r
```
- Help Section:
```python
python exploit.py -h
```
Or
```bash
bash exploit.sh -h
```

## Prerequisites
Before running the exploit, ensure the following:
- Sudo Version: The target system must be running a vulnerable version of sudo. The script checks for versions between 1.8.0 and 1.9.12p1.0
- Sudo Privileges: The current user must have the ability to run sudoedit or sudo -e on files as root.

## Notes
- The script attempts to open the /etc/sudoers file using vim if the user is found to be exploitable.
- Important: Use this script only on systems where you have explicit permission to test for vulnerabilities. Unauthorized use of this script is illegal and unethical.


## Author
- Author: D0rDa4aN919

## License
- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



