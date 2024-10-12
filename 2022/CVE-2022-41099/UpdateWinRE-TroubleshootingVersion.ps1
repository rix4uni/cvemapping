# Script by Brandon Halsey
# https://github.com/halsey51013/UpdateWindowsRE-CVE-2022-41099
# Script to update Windows Recovery Environment to patch against CVE-2022-41099. 
# Supported OS and Builds: Windows 11 (22H2 & 21H2) & Windows 10 (22H2, 21H2, 21H1, & 20H2). Unsure if LTSC will work. 
# Built with help from comments of reddit users /u/shiz0_ and /u/DrunkMAdmin and u/JoseEspitia_com
# No warranty implied. Do your own testing prior to running.

# -----WARNING-----
#Do not use this for normal updating! This version is without all the checks and error handling to aid in troubleshooting. This should be ran line by line manually.
# -----WARNING-----



$WinOSBuild = [System.Environment]::OSVersion.Version.Build
if ($WinOSBuild -eq 22621) {
    Write-Host "Windows 11 22H2 - Build 22621"
    #2023-01 Cumulative Update KB5022303
    $MSUPatch = "https://catalog.s.download.windowsupdate.com/d/msdownload/update/software/secu/2023/01/windows11.0-kb5022303-x64_87d49704f3f7312cddfe27e45ba493048fdd1517.msu"
} elseif ($WinOSBuild -eq 22000) {
    Write-Host "Windows 11 21H2 - Build 22000"
    #2023-01 Cumulative Update KB5022287
    $MSUPatch = "https://catalog.s.download.windowsupdate.com/d/msdownload/update/software/secu/2023/01/windows10.0-kb5022287-x64_55641f1989bae2c2d0f540504fb07400a0f187b3.msu"
} elseif ($WinOSBuild -eq 19045) {
    Write-Host "Windows 10 22H2 - Build 19045"
    #2023-01 Cumulative Update KB5022282
    $MSUPatch = "https://catalog.s.download.windowsupdate.com/d/msdownload/update/software/secu/2023/01/windows10.0-kb5022282-x64_fdb2ea85e921869f0abe1750ac7cee34876a760c.msu"
} elseif ($WinOSBuild -eq 19044) {
    Write-Host "Windows 10 21H2 - Build 19044"
    #2023-01 Cumulative Update KB5022282
    $MSUPatch = "https://catalog.s.download.windowsupdate.com/d/msdownload/update/software/secu/2023/01/windows10.0-kb5022282-x64_fdb2ea85e921869f0abe1750ac7cee34876a760c.msu"
} elseif ($WinOSBuild -eq 19043) {
    Write-Host "Windows 10 21H1 - Build 19043"
    #2022-12 Cumulative Update KB5021233 -- OS out of support and latest patch is December
    $MSUPatch = "https://catalog.s.download.windowsupdate.com/d/msdownload/update/software/secu/2022/12/windows10.0-kb5021233-x64_00bbf75a829a2cb4f37e4a2b876ea9503acfaf4d.msu"
} elseif ($WinOSBuild -eq 19042) {
    Write-Host "Windows 10 20H2 - Build 19042"
    #2023-01 Cumulative Update KB5022282
    $MSUPatch = "https://catalog.s.download.windowsupdate.com/d/msdownload/update/software/secu/2023/01/windows10.0-kb5022282-x64_fdb2ea85e921869f0abe1750ac7cee34876a760c.msu"
} else {
    throw "OS Build Number not recognized/supported by script. Only Windows 11 (22H2 & 21H2) & Windows 10 (22H2, 21H2, 21H1, & 20H2) supported."
}


Invoke-WebRequest -Uri $MSUPatch -OutFile "C:\Windows\Temp\WinREFix.msu"
New-Item -ItemType Directory -Path "C:\mount" -Force
ReAgentC.exe /mountre /path c:\mount
Dism /Add-Package /Image:C:\mount\ /PackagePath:"C:\Windows\Temp\WinREFix.msu"
dism /image:C:\mount /cleanup-image /StartComponentCleanup /ResetBase
ReAgentC.exe /unmountre /path c:\mount /commit
Remove-Item -Path "C:\mount" -Force
Remove-Item -Path "C:\Windows\Temp\WinREFix.msu" -Force
