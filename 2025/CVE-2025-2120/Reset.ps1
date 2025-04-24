function Write-Status {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true, Position=0)]
        [ValidateSet("INFO", "ACTION", "OK", "FAIL", "WARN", IgnoreCase=$true)]
        [string] $Status,

        [Parameter(Mandatory=$true, Position=1)]
        [ValidateNotNullOrEmpty()]
        [string] $Message,

        [int] $Indent = 0
    )

        $okPrefix = "[OK]"
        $failPrefix = "[FAIL]"
        $warningPrefix = "[WARN]"
        $actionPrefix = "[>>]"
        $infoPrefix = "[i]"

        switch ($Status.ToUpperInvariant()) {
            "ACTION" {$prefix=$actionPrefix;$colour="Blue"}
            "OK" {$prefix=$okPrefix;$colour="Green"}
            "FAIL" {$prefix=$failPrefix;$colour="Red"}
            "WARN" {$prefix=$warningPrefix;$colour="Yellow"}
            "INFO" {$prefix=$infoPrefix; $colour="White"}
            default {$prefix=$null; $colour="White"}
        }

        if ($Indent -gt 0) {
            Write-Host ("`t" * $Indent) -NoNewline
        }

        if ($prefix) {
            Write-Host $prefix -ForegroundColor $colour -NoNewline
            $Message = " $Message"
        }

        Write-Host $Message
}

function Test-IsAdminElevated {
    return ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::
            GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
}

function Get-ElevatedTerminal {

    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$OriginalParameters,
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$ScriptPath
    )

    if (Test-IsAdminElevated) {
        return
    }

    # Sanity check script path
    if (!((Test-Path -Path $ScriptPath -PathType Leaf) -and $ScriptPath -match "\.ps1$" )) {
        throw "Path not found or invalid PS1 file: $ScriptPath"
    }

    $baseArguments = @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", "`"$ScriptPath`""
    )

    Write-Status -Status WARN -Message "Attempting to relaunch the script with elevated privileges..."

    $additionalArgs = @()

    if ($OriginalParameters.Count -gt 0) {
        foreach ($param in $OriginalParameters.GetEnumerator()){
            $key = $param.Key
            $value = $param.Value

            if ($value -is [switch]) {
                if ($value.IsPresent) {
                    $additionalArgs += "-$key"
                }
            } elseif ($null -eq $value) {
                $additionalArgs += "-$key"
            } else {
                $formattedValue = "`"$value`""
                $additionalArgs += "-$key", $formattedValue
            }
        }
    }

    $cmdToRun = ""
    $finalArgumentList = @()

    if (Get-Command wt.exe -ErrorAction SilentlyContinue) {
        $cmdToRun = "wt.exe"
        $finalArgumentList = @(
            "new-tab",
            "-p",
            "powershell",
            "powershell.exe"
        ) + $baseArguments + $additionalArgs
    } else {
        $cmdToRun = "powershell.exe"
        $finalArgumentList = $baseArguments + $additionalArgs
    }

    try {
        Start-Process $cmdToRun -ArgumentList $finalArgumentList -Verb RunAs -ErrorAction Stop
        exit 0
    }
    catch {
        Write-Error "Failed to start elevated process: $($_.Exception.Message)"
        exit 1
    }
}

Clear-Host

if (-not(Test-IsAdminElevated)) {
    Get-ElevatedTerminal -OriginalParameters $PSBoundParameters -ScriptPath $MyInvocation.MyCommand.Path
}

# Permissions as of 24/04/25
$aclImportString = @"
inetpub
D:P(A;;FA;;;S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464)(A;OICIIO;GA;;;S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464)(A;;FA;;;SY)(A;OICIIO;GA;;;SY)(A;;FA;;;BA)(A;OICIIO;GA;;;BA)(A;;0x1200a9;;;BU)(A;OICIIO;GXGR;;;BU)(A;OICIIO;GA;;;CO)
"@

# SYSTEMDRIVE:\inetpub
$targetPath = Join-Path -Path $env:SystemDrive -ChildPath "inetpub"

try {
    # Create the directory if it doesn't exist.
    if (!(Test-Path -Path $targetPath -PathType Container)) {
        try {
            Write-Status -Status ACTION -Message "Creating directory '$targetPath'..."
            New-Item -Path $targetPath -ItemType Directory -Force -ErrorAction Stop | Out-Null
            Write-Status -Status OK -Message "Directory created."
        }
        catch {
            throw "Unable to to create directory: $targetPath"
        }
    } else {
        Write-Status -Status OK -Message "Target directory '$targetPath' already exists."
    }

    Write-Status -Status ACTION -Message "Taking ownership of '$targetPath'..."

    # Transfer ownership of the directory to the "Administrators" group.
    $null = takeown /F $targetPath /A /R /D Y

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to take ownership of '$targetPath'. (Exit code $LASTEXITCODE). Unable to proceed."
    }

    Write-Status -Status OK -Message "Ownership successfully granted to the Administrators group."

    try {
        Write-Status -Status ACTION -Message "importing necessary permissions..."

        # Create a temporary file for use with icacls restore.
        $aclFile = New-TemporaryFile -ErrorAction Stop
        Set-Content -Value $aclImportString -Path $aclFile -Encoding unicode -Force -ErrorAction Stop

        # icacls "C:\" /restore path\to\file.tmp
        $null = icacls "$env:SystemDrive\" /restore $aclFile.FullName

        if ($LASTEXITCODE -ne 0) { throw } else {
            Write-Status -Status OK -Message "Permissions successfully imported."
        }
    } catch {
        throw "Failed to apply permissions using Set-ACL for: '$targetPath'. Error: $($_.Exception.Message)"
    } finally {
        # Remove the temporary file.
        $aclFile | Remove-Item -Force -ErrorAction SilentlyContinue
    }

    Write-Status -Status ACTION -Message "Setting owner to 'NT AUTHORITY\SYSTEM'..."

    try {
        # Set the owner of inetpub to 'NT AUTHORITY\SYSTEM'.
        $null = icacls $targetPath /SetOwner "SYSTEM"

        if ($LASTEXITCODE -ne 0) { throw } else {
            Write-Status -Status OK -Message "Owner successfully changed."
        }
    }
    catch {
        throw "Failed to set owner for '$targetPath'. Error: $($_.Exception.Message)"
    }
} catch {
    Write-Status -Status FAIL -Message $_.Exception.Message
    exit 1
} finally {
    Write-Host ("-" * 25)
    Write-Status -Status OK -Message "Script execution complete."
    Write-Status -Status INFO -Message "Press any key to continue..."
    # Pause on exit.
    $null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}