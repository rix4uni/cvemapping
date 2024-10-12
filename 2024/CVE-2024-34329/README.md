# CVE-2024-34329
Tested Product: Datacard XPS Card Printer Driver Version: <= 8.4

Description: The application is prone to Local Privilege Escalation (LPE) vulnerability due to insecure file/folder permissions on its default installation, by which it grants the rights for everyone for full control over the path: C:\ProgramData\Datacard\XPS Card Printer\Service. Files and folders in the path "C:\ProgramData\Datacard" can be modified by unprivileged users, malicious processes and/or threat actors. Once an admin installs XPS Card Printer, which runs under SYSTEM context, it will invoke the DEVOBJ.dll or CFGMGR32.dll in the directory "C:\ProgramData\Datacard\XPS Card Printer\Service", where a low privileged user can already place a malicious dll upfront and which will not be checked and deleted by the installation. These dlls do not exist and therefore will give NOT FOUND by the application installer. If a malicious user places a dll named DEVOBJ.dll or CFGMGR32.dll within this directory, the setup will inadvertently execute these malicious dll when the service is trying to connect to the card printer, running them with SYSTEM privileges.

Exploit POC:

1- With a low priv user, create the directory "C:\ProgramData\Datacard\XPS Card Printer\Service" and throw a desired DLL and rename it to DEVOBJ.dll or CFGMGR32.dll

2- With an Administrator, proceed to install the driver as normal.

3- The DLL payload will be executed as SYSTEM.
