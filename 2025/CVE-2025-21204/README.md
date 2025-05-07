# Reset inetpub

This script restores the `%SYSTEMDRIVE%\inetpub` folder and its default security permissions, which are necessary as a mitigation for [CVE-2025-21204](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-21204) following the [KB5055523](https://support.microsoft.com/en-gb/topic/april-8-2025-kb5055523-os-build-26100-3775-277a9d11-6ebf-410c-99f7-8c61957461eb) Windows update.

It's intended for users who may have deleted this folder before understanding its security purpose and wish to restore it without needing to enable/disable IIS features.

## What This Script Does

1.  Creates the `%SYSTEMDRIVE%\inetpub` directory if it does not exist.
2.  Applies the default Access Control List (ACL) permissions required for the security mitigation to the `inetpub` folder itself.
3.  Sets the owner of the `inetpub` folder to `NT AUTHORITY\SYSTEM`.

## Prerequisites

*   **Administrator privileges are required** to modify system folders and permissions.

## Usage Instructions

Choose **one** of the following methods. All require an **elevated (Administrator) PowerShell** window.

### Method 1: Quick Execution (Pause on Completion)

This command downloads and runs the script immediately. The script will pause for confirmation upon completion by default.

```powershell
powershell -ExecutionPolicy Bypass -Command "irm 'https://raw.githubusercontent.com/mmotti/Reset-inetpub/refs/heads/main/Reset.ps1' | iex"
```

### Method 2: Quick Execution (No Pause)

This command downloads and runs the script immediately, using the `-NoWait` switch to prevent the script from pausing upon completion.

```powershell
powershell -ExecutionPolicy Bypass -Command "& ([ScriptBlock]::Create((irm 'https://raw.githubusercontent.com/mmotti/Reset-inetpub/refs/heads/main/Reset.ps1'))) -NoWait"
```

*   `-NoWait`: A switch parameter passed to the script to suppress the final "Press any key to continue..." prompt.

### Method 3: Manual Execution

1.  **Download the script:**
    ```powershell
    $scriptPath = Join-Path $env:TEMP "Reset-inetpub.ps1"
    Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/mmotti/Reset-inetpub/refs/heads/main/Reset.ps1' -OutFile $scriptPath
    ```
2.  **(Optional) Review the script:**
    ```powershell
    # Open in Notepad
    notepad $scriptPath
    ```
3.  **Execute the local script:**
    ```powershell
    # Standard execution (will pause at the end)
    powershell -ExecutionPolicy Bypass -File $scriptPath

    # -- OR -- #

    #Execution without the final pause
    powershell -ExecutionPolicy Bypass -File $scriptPath -NoWait
    ```
4.  **(Optional) Clean up the downloaded script:**
    ```powershell
    Remove-Item -Path $scriptPath -Force
    ```

---

## Scope and Limitations

Please be aware of the following:

*   **Parent Folder Only:** The script primarily targets the permissions and ownership of the `%SYSTEMDRIVE%\inetpub` folder itself. Default inheritance settings are applied.
*   **Existing Content Warning:** If the `inetpub` directory exists and contains files or subfolders, the script will:
    *   Warn you that the directory is not empty.
    *   Proceed to apply the default permissions to the `inetpub` folder.
    *   Apply the ownership change (`NT AUTHORITY\SYSTEM`) *only* to the `inetpub` folder itself, not recursively. This avoids potentially overriding custom permissions on existing sub-content.

## Permissions Details

The script aims to apply the following permissions, captured from a clean `inetpub` directory created by the relevant Windows update.

**`icacls` export:** See [acls.txt](acls.txt) for the raw SDDL string used by the script.

**`icacls` permission summary (example from `C:` drive):**

```plaintext
C:\inetpub NT SERVICE\TrustedInstaller:(F)
           NT SERVICE\TrustedInstaller:(OI)(CI)(IO)(F)
           NT AUTHORITY\SYSTEM:(F)
           NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
           BUILTIN\Administrators:(F)
           BUILTIN\Administrators:(OI)(CI)(IO)(F)
           BUILTIN\Users:(RX)
           BUILTIN\Users:(OI)(CI)(IO)(GR,GE)
           CREATOR OWNER:(OI)(CI)(IO)(F)
```

*(Note: The script dynamically determines the correct drive letter.)*