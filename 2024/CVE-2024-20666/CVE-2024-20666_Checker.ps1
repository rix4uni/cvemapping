<#
.SYNOPSIS
Checks the WinRE environment on the local machine to see if it has been patched against CVE-2024-20666

.DESCRIPTION
Runs the reagentc command to get the WinRE path. Then runs DISM to get the version and build.
The version and build are checked against the values listed in the CVE to ensure that the
WinRE environment has been patched.


.LINKS
https://msrc.microsoft.com/update-guide/vulnerability/CVE-2024-20666
https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/add-update-to-winre?view=windows-11#check-the-winre-image-version
#>

# This array was built off the information in CVE-2024-20666 as of 1/10/2024
$affectedBuilds = @(
    [pscustomobject]@{Product = 'Windows Server 2016'; Version = '10.0.14393'; Build = 6614}
    [pscustomobject]@{Product = 'Windows 10 Version 1607'; Version = '10.0.14393'; Build = 6614}
    [pscustomobject]@{Product = 'Windows 10'; Version = '10.0.10240'; Build = 20402}
    [pscustomobject]@{Product = 'Windows Server 2022, 23H2 Edition'; Version = '10.0.25398'; Build = 643}
    [pscustomobject]@{Product = 'Windows 11 Version 23H2'; Version = '10.0.22631'; Build = 3007}
    [pscustomobject]@{Product = 'Windows 10 Version 22H2'; Version = '10.0.19045'; Build = 3930}
    [pscustomobject]@{Product = 'Windows 11 Version 22H2'; Version = '10.0.22621'; Build = 3007}
    [pscustomobject]@{Product = 'Windows 10 Version 21H2'; Version = '10.0.19044'; Build = 3930}
    [pscustomobject]@{Product = 'Windows 11 version 21H2'; Version = '10.0.22000'; Build = 2713}
    [pscustomobject]@{Product = 'Windows Server 2022'; Version = '10.0.20348'; Build = 2227}
    [pscustomobject]@{Product = 'Windows Server 2019'; Version = '10.0.17763'; Build = 5329}
    [pscustomobject]@{Product = 'Windows 10 Version 1809'; Version = '10.0.17763'; Build = 5329}
)

# Get the OS Version
$OSVersion = [Environment]::OSVersion.Version.ToString() | ForEach-Object{ $_.Substring(0,$_.LastIndexOf('.')).Trim() }

# Run reagentc to get the path to the WinRE volume
$info = reagentc /info
$path = $info | Where-Object{ $_ -match 'Windows RE location:' } | ForEach-Object{ $_.Substring($_.IndexOf(':')+1).Trim() }
if([string]::IsNullOrEmpty($path)){
    throw "The expected information was not returned from reagentc. Ensure you are running with admin permissions. `n  reagentc: $($info)"
}

# Run Dism to get the information about the partition
$winre = Invoke-Expression "Dism /Get-ImageInfo /ImageFile:$($path)\winre.wim /index:1"

# Extract the version and build from the output
$WinREVersion = $winre | Where-Object{ $_ -match '^Version :' } | ForEach-Object{ $_.Substring($_.IndexOf(':')+1).Trim() }
[int]$Build = $winre | Where-Object{ $_ -match '^ServicePack Build :' } | ForEach-Object{ $_.Substring($_.IndexOf(':')+1).Trim() }

# Check the version and build against the affected versions
$affected = $affectedBuilds | Where-Object{ $_.Version -eq $OSVersion }
if(-not $affected){
    Write-Host "Windows version '$($OSVersion)' was not listed in 'CVE-2024-20666'`nYou could be on an unsupported version of Windows. You will want to manually verify." -ForegroundColor Yellow
}
elseif($Build -ge $affected.Build){
    Write-Host "Your WinRE has been patched against 'CVE-2024-20666'" -ForegroundColor Green
}
else{
    Write-Host "Your WinRE has NOT been patched against 'CVE-2024-20666'" -ForegroundColor Red
    Write-Host "Build number: '$($WinREVersion).$($Build)' is lower than the expected value of '$($affected.Version).$($affected.Build)'" -ForegroundColor Red
}
