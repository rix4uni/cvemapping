<#
.SYNOPSIS
Restores the %SYSTEMDRIVE%\inetpub directory and resets its default security permissions and ownership.

.DESCRIPTION
This script addresses the creation of the %SYSTEMDRIVE%\inetpub directory introduced by Windows update KB5055523 as a mitigation for CVE-2025-21204.
It facilitates the restoration of this directory and its required permissions for users who may have previously deleted it, without necessitating the enablement or disablement of IIS features.

The script performs the following actions:
1. Ensures the %SYSTEMDRIVE%\inetpub directory exists, creating it if absent.
2. Applies the standard Access Control List (ACL) permissions to the %SYSTEMDRIVE%\inetpub directory, using the settings captured after the installation of KB5055523. This action overwrites existing permissions on the directory itself.
3. Sets the owner of the %SYSTEMDRIVE%\inetpub directory to 'NT AUTHORITY\SYSTEM'.

Important Considerations:
- If the directory already contains files or subdirectories, the permission reset and ownership change will only apply directly to the %SYSTEMDRIVE%\inetpub directory itself. Inheritance will apply standard rules, but existing child item permissions are not forcefully overwritten, and ownership of child items is not changed.
- The script requires elevation (Run as Administrator) to modify system directories and permissions.

.PARAMETER NoWait
Suppresses the final "Press any key to continue..." prompt, causing the script to exit immediately upon completion without waiting for user input.

.EXAMPLE
PS C:\> .\Reset.ps1

Description:
-----------
Executes the script. It will create or verify the inetpub directory, apply the necessary permissions and ownership, display status messages, and pause for confirmation upon completion. Requires an elevated PowerShell session.

.EXAMPLE
PS C:\> .\Reset.ps1 -NoWait

Description:
-----------
Executes the script in the same manner as the first example, but the -NoWait switch prevents the script from pausing at the end. It will exit immediately after displaying the final status message. Requires an elevated PowerShell session.

.NOTES

Author: mmotti (https://github.com/mmotti)
Requires:    Windows PowerShell 5.1 or later.
Requires:    Administrator privileges.
Warning:     This script modifies file system permissions and ownership on the %SYSTEMDRIVE%\inetpub directory. Ensure you understand the changes before execution.

.LINK
GitHub Repository: https://github.com/mmotti/Reset-inetpub
KB5055523: https://support.microsoft.com/en-gb/topic/april-8-2025-kb5055523-os-build-26100-3775-277a9d11-6ebf-410c-99f7-8c61957461eb
CVE-2025-21204: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-21204
#>
#Requires -RunAsAdministrator

param (
    [Parameter()]
    [switch] $NoWait
)

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

Clear-Host

# SYSTEMDRIVE:\inetpub
$targetPath = Join-Path -Path $env:SystemDrive -ChildPath "inetpub"

# Permissions as of 24/04/25
$aclImportString = @"
$(Split-Path -Path $targetPath -Leaf)
D:PAI(A;;FA;;;S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464)(A;OICIIO;GA;;;S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464)(A;;FA;;;SY)(A;OICIIO;GA;;;SY)(A;;FA;;;BA)(A;OICIIO;GA;;;BA)(A;;0x1200a9;;;BU)(A;OICIIO;GXGR;;;BU)(A;OICIIO;GA;;;CO)S:AINO_ACCESS_CONTROL
"@

# Comparison string for icacls (Get-Acl Sddl is not reliable for this).
$aclComparisonArray = @"
C:\inetpub NT SERVICE\TrustedInstaller:(F)
           NT SERVICE\TrustedInstaller:(OI)(CI)(IO)(F)
           NT AUTHORITY\SYSTEM:(F)
           NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
           BUILTIN\Administrators:(F)
           BUILTIN\Administrators:(OI)(CI)(IO)(F)
           BUILTIN\Users:(RX)
           BUILTIN\Users:(OI)(CI)(IO)(GR,GE)
           CREATOR OWNER:(OI)(CI)(IO)(F)
"@  -replace '(?m)^[A-Z]:(\\inetpub)', "$env:SYSTEMDRIVE`$1" -split '\r?\n'

$aclChangeRequired = $false
$aclOwnerChangeRequired = $false
$expectedOwner = "NT AUTHORITY\SYSTEM"
$scriptErrorOccurred = $false

try {
    # Directory doesn't exist.
    if (-not(Test-Path -Path $targetPath -PathType Container)) {
        try {
            Write-Status -Status ACTION -Message "Creating directory '$targetPath'"
            New-Item -Path $targetPath -ItemType Directory -Force -ErrorAction Stop | Out-Null
            $aclChangeRequired = $true; $aclOwnerChangeRequired = $true
            Write-Status -Status OK -Message "Directory created." -Indent 1
        }
        catch {
            throw "Unable to create directory: $targetPath"
        }
    # Directory exists.
    } else {
        try {
            Write-Status -Status ACTION -Message "Checking permissions of '$targetPath'"

            $icaclsCurrent = icacls "$targetPath"
            if ($LASTEXITCODE -ne 0) { throw }


            $icaclsMatch = Compare-Object -ReferenceObject ($aclComparisonArray | ForEach-Object {$_.Trim()} | Where-Object {$_.Length -gt 0}) `
                                          -DifferenceObject ($icaclsCurrent | Select-Object -SkipLast 2 | ForEach-Object {$_.Trim()} | Where-Object {$_.Length -gt 0}) `
                                          -IncludeEqual | Where-Object {$_.SideIndicator -ne "=="}


            if (-not ($null -eq $icaclsMatch)) {
                Write-Status -Status WARN -Message "Permissions require updating." -Indent 1
                $aclChangeRequired = $true
            } else {
                Write-Status -Status OK -Message "Permissions verified." -Indent 1
            }

            Write-Status -Status ACTION -Message "Checking the owner of '$targetPath'"

            $currentOwner = (Get-Acl $targetPath -ErrorAction Stop).Owner

            if ($currentOwner -ine $expectedOwner) {
                Write-Status -Status WARN -Message "Ownership requires updating." -Indent 1
                $aclOwnerChangeRequired = $true
            } else {
                Write-Status -Status OK -Message "Ownership verified." -Indent 1
            }
        }
        catch {
            Write-Status -Status WARN -Message "Unable to determine current permissions. Assuming an update is required." -Indent 1
            $aclChangeRequired = $true; $aclOwnerChangeRequired = $true
        }
    }

    # Early exit if we've determined that no changes are required.
    if (-not ($aclChangeRequired -or $aclOwnerChangeRequired)) {
        Write-Status -Status OK -Message "No changes are required."
        exit 0
    } else {

        Write-Status -Status ACTION -Message "Checking contents of '$targetPath'"

        # If the directory isn't empty, provide a warning of the limited scope of the changes.
        if (Get-ChildItem -Path $targetPath -ErrorAction SilentlyContinue) {
            Write-Status -Status WARN -Message "'$targetPath' is not empty!" -Indent 1
            Write-Status -Status WARN -Message "Ownership and direct permission changes (default settings) will only apply to the parent directory ($targetPath) and will not be applied recursively." -Indent 1
            Write-Status -Status WARN -Message "However, inheritable permissions from the parent will propagate to subdirectories as expected." -Indent 1
            Write-Status -Status WARN -Message "This approach helps prevent potential issues with manually applied permissions." -Indent 1

        # Directory exists and is empty.
        } else {
            Write-Status -Status OK -Message "'$targetPath' exists and is empty." -Indent 1
        }

        if ($aclChangeRequired) {
            try {
                Write-Status -Status ACTION -Message "Importing necessary permissions"

                # Create a temporary file for use with icacls restore.
                $aclFile = New-TemporaryFile -ErrorAction Stop
                Set-Content -Value $aclImportString -Path $aclFile -Encoding unicode -Force -ErrorAction Stop

                # icacls "C:\" /restore path\to\file.tmp
                $result = icacls "$env:SystemDrive\" /restore $aclFile.FullName 2>&1

                if ($LASTEXITCODE -ne 0) { throw $result } else {
                    Write-Status -Status OK -Message "Permissions successfully imported." -Indent 1
                }
            } catch {
                throw "Failed to import permissions for '$targetPath'. Error $($_.Exception.Message)."
            } finally {
                # Remove the temporary file.
                $aclFile | Remove-Item -Force -ErrorAction SilentlyContinue
            }
        }
        
        if ($aclOwnerChangeRequired) {
            try {
                Write-Status -Status ACTION -Message "Setting owner of '$targetPath' to '$expectedOwner'"

                # Set the owner of inetpub to 'NT AUTHORITY\SYSTEM'.
                $result = icacls $targetPath /SetOwner "SYSTEM" 2>&1

                if ($LASTEXITCODE -ne 0) { throw $result } else {
                    Write-Status -Status OK -Message "Owner successfully set." -Indent 1
                }
            }
            catch {
                throw "Failed to set owner for '$targetPath'. Error: $($_.Exception.Message)"
            }
        }
    }

} catch {
    Write-Status -Status FAIL -Message $_.Exception.Message -Indent 1
    $scriptErrorOccurred = $true
} finally {

    Write-Host

    $statusParams = @{ Status = if ($scriptErrorOccurred) { "FAIL" } else { "OK" }; Message = if ($scriptErrorOccurred) { "Script execution completed with error(s)." } else { "Script execution completed successfully." } }
    Write-Status @statusParams

    # Pause on exit.
    if (-not($NoWait)) {
        Write-Status -Status ACTION -Message "Press any key to continue..."
        $null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

# Conditional exit code based on whether an error occurred.
switch ($scriptErrorOccurred) {
    $true {exit 1}
    $false {exit 0}
}