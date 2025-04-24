# Reset inetpub

[KB5055523](https://support.microsoft.com/en-gb/topic/april-8-2025-kb5055523-os-build-26100-3775-277a9d11-6ebf-410c-99f7-8c61957461eb) has introduced the creation of an `inetpub` folder at `%SYSTEMDRIVE%\inetpub` as a mitigation for [CVE-2025-2120](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-21204).

If, like me, you deleted this folder before realizing its purpose in addressing security concerns, this guide is for you.

The procedure outlined here enables you to restore the folder and configure the appropriate permissions (at least for the parent folder), without needing to enable and disable IIS.

Please note: **Administrator privileges are required**.

## Instructions

1. Clone this repo (or download / extract) to your desired location.
2. Execute `Run.bat`.

## Script Actions
1. Create `%SYSTEMDRIVE%\inetpub` if it doesn't exist.
1. Assign temporary ownership of the directory to the `BUILTIN\Administrators` group.
1. Import the appropriate ACL permissions.
1. Assign ownership of the directory to `NT AUTHORITY\SYSTEM`.

## Permissions
    C:\inetpub NT SERVICE\TrustedInstaller:(F)
           NT SERVICE\TrustedInstaller:(OI)(CI)(IO)(F)
           NT AUTHORITY\SYSTEM:(F)
           NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
           BUILTIN\Administrators:(F)
           BUILTIN\Administrators:(OI)(CI)(IO)(F)
           BUILTIN\Users:(RX)
           BUILTIN\Users:(OI)(CI)(IO)(GR,GE)
           CREATOR OWNER:(OI)(CI)(IO)(F)
