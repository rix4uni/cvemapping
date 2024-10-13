# CABTrap_OneNote2007
Microsoft Office Onenote 2007 (CVE-2014-2815) ".ONEPKG" File Directory Traversal Vulnerability Leads to Arbitrary Code Execution
Microsoft Office Onenote 2007 (CVE-2014-2815) ".ONEPKG" File Directory Traversal Vulnerability Leads to Arbitrary Code Execution

OneNote 2007 is prone to a vulnerability that causes the program to extract files contained inside a ".onepkg"
file,which uses the "MS CAB Format", to be extracted to an arbitrary location in the system by using parent directory 
"\..\" in the file names.
Since Onenote also does not check file extensions, it is possible to extract unsafe files to arbitrary locations. 

On Windows XP the standard user has write access to most locations in the system, so an attacker is able to extract a DLL
file (ntshrui.dll) to Microsoft Office install dir which gets loaded by Onenote just after processing the ".onepkg" file:

c:\program files\microsoft office\office12\ntshrui.dll

On Windows Vista and above the standard user is limited by the "UAC" feature so that it is only possible to extract files to the 
current user´s profile sub directories. Extracting an executable file to the startup folder is possible, which leads to
arbitrary code execution as well, when the computer is re-started.

To reproduce this, use a Cab archiver software (eg. 'makecab.exe') or your IDE with programming language of choice that supports
the MS CAB format, and insert files with long names inside a new cab archive. 
 and edit the file names by replacing the characters with parent directories "\..\".
Rename the produced cab archive to ".onepkg".

in this PoC, Windows Write app was used, and to be dropped in startup folder, I named it:

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaWrite.exe

then by using the traversal technique, the file name inside the CAB archive becomes:

..\..\..\roaming\microsoft\windows\start menu\programs\startup\Write.exe


Vulnerable: MS Office 2007 SP3
Tested on: Windows XP SP3, Vista SP2, 7 SP1 + Office 2007 SP3 (without the patch)
(other OSes will likely be vulnerable as well)
