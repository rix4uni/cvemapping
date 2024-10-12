Affected application: QlikView 
Platform: Windows
Issue: Local Privilege Escalation via MSI installer (DLL hijacking race condition)
Discovered and reported by: Pawel Karwowski and Julian Horoszkiewicz (Eviden Red Team)

Details:
On systems with QuikView12 installed, it is possible for regular users to trigger the installer in "repair" mode, by issuing the following command:
msiexec.exe /fa PATH_TO_INSTALLER_FILE.msi

This triggers the msiexec service, which carries the repair process, running multiple actions and, between others, creates files inside C:\Users\pk\AppData\Local\Temp directory, which have their filenames dynamically generated, in following template: "wac<four random letters or numbers>.tmp", for example, wac98DF.tmp. 

The process then uses the generated wac****.tmp file (executable) running as NT AUTHORITY/SYSTEM to write to, and load an image of itself. 

Since the C:\Users\pk\AppData\Local\ directory is owned by the regular user, the C:\Users\pk\AppData\Local\Temp\ directory inherits the permissions, making it possible for the regular user to interfere with the contents of the directory, for example by overwriting the dynamically generated DLL files.
This creates a race condition. If manages to locate the DLL file, they can attempt to overwrite them with their own file. If they manage to perform the replacement in the correct (very narrow) time window - right after the original file has been written by the installer and the file descriptor has been closed, but before the installer calls LoadLibrary() on it, they can get their own DLL file executed as NT AUTHORITY/SYSTEM, creating a Local Privilege Escalation.

Exploitation is done with the use of a powershell script that runs the .MSI file, checks for the presence and creation of our legit EXE of interest, and repeatedly copies my Proof of Concept EXE into the Appdata\Local\Temp directory, effectively overwriting the legit EXE file. After being loaded, the PoC EXE file creates a poc.txt file in C:\Users\Public, together with the command line that called it, and whoami output. 

MSI file SHA256 sum:
0267324393384ED2B0746D6CEBDD0FD7D8DBD26853BDA58F875F20F40EBBB898 
