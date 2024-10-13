# PoC for CVE-2021-26088 written in PowerShell

## Description

> An improper authentication vulnerability in FSSO Collector may allow an unauthenticated user to bypass any firewall authentication rule and access the protected network via sending specifically crafted UDP login notification packets.

https://www.fortiguard.com/psirt/FG-IR-20-191

## Content

- forge_auth.ps1: main exploit
- check_src_port.ps1: get the source port range assigned to the current user

 ## Disclaimer

The tool provided in this repository is intended for educational and research purposes only. The author does not condone and is not responsible for any illegal activities performed with this tool. The user is solely responsible for any consequences of using this tool. The author makes no warranties, express or implied, regarding the tool's performance, reliability, or suitability for any particular purpose. The tool is provided "as is" without any warranty of any kind, either expressed or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. The author shall not be liable for any damages whatsoever arising out of the use or inability to use this tool, even if the author has been advised of the possibility of such damages.

It is important to note that using a tool like this to exploit vulnerabilities without explicit permission is illegal and unethical. It is strongly recommended that you use this tool only in a controlled environment and with the appropriate permissions