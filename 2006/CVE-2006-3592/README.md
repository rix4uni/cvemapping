# CVE-2006-3952
Exploit for Easy File Sharing FTP Server 3.5 on Win7 32


Based on:
* pwntools
* msfvenom / reverse\_tcp payload

Vulnerable app available at https://www.exploit-db.com/apps/0efddb6d04f4125d7c1f104c6b1c60a0-efsfs.exe

Simple SEH overrite + couple jumps back, due to stack being corrupted after SEH value.
