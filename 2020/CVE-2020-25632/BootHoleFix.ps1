$banner = @"
                         
    This script will remediate the BootHole bug
    identified in CVE-2020-25632 and/or
    CVE-2021-20233.
    
    On July 29, 2020, Microsoft published security
    advisory 200011 that describes a new
    vulnerability that's related to Secure Boot.
    Devices that trust the Microsoft third-party
    Unified Extensible Firmware Interface (UEFI)
    Certificate Authority (CA) in their Secure Boot
    configuration may be susceptible to an attacker
    who has administrative privileges or physical
    access to the device.

    This script is to apply the latest Secure Boot
    DBX revocation list to invalidate the vulnerable
    modules. 

    Paul Rowland - 2022

    v1.0 - 19/07/2022

"@

Write-Host $banner

Start-Sleep -Seconds 2

Write-Host -ForegroundColor Yellow @"


    Applying BootHole fix. Please wait until the script
    has completed as this may take some time...


"@

$originalDIR = $PSScriptRoot
$workDIR = "C:\Windows\Temp\BootHoleFix"
$dbxFileURi =  "https://uefi.org/sites/default/files/resources/dbxupdate_x64.bin"
$dbxFile = "$workDIR\dbxupdate_x64.bin"
$splitScriptURI = "https://psg-prod-eastus.azureedge.net/packages/splitdbxcontent.1.0.0.nupkg"
$splitScriptPKG = "$workDIR\SplitDbxContent.zip"
$splitScript = "$workDIR\SplitDbxContent.ps1"
$contentBIN = "$workDIR\content.bin"
$signatureP7 = "$workDIR\Signature.p7"

if (!(Test-Path $workDIR)) { New-Item -ItemType Directory -Path "C:\Windows\Temp" -Name "BootHoleFix"}

Invoke-WebRequest -Uri $dbxFileURi -OutFile $dbxFile

Invoke-WebRequest -Uri $splitScriptURI -OutFile $splitScriptPKG

Expand-Archive -Path $splitScriptPKG -DestinationPath $workDIR -Force

Set-Location $workDIR

& "$splitScript" "$dbxFile"


Set-SecureBootUEFI -Name dbx -ContentFilePath $contentBIN -SignedFilePath $signatureP7 -Time 2010-03-06T19:17:21Z -AppendWrite

Set-Location $originalDIR

Write-Host -ForegroundColor Green @"


    Complete, you may now close this window...


"@
