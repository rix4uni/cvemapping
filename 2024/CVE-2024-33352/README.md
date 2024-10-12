**CVEID**: CVE-2024-33352

**Bluestacks Advisory ID**: pending

**Name of the affected product(s) and version(s)**: BlueStacks for Windows (versions prior to 10.40.1000.502)

**Vulnerability type**:  CWE-552: Files or Directories Accessible to External Parties

---

**Summary**

BlueStacks is an Android emulator which runs the guest Android system within a virtual machine. Because BlueStacks
stores virtual machine configuration files in a world-writeable directory and shares them across different OS users,
it is possible for an unprivileged user to backdoor an image that would then gain code execution capabilities
of a privileged user.

**Description**
 
BlueStacks configuration is stored globally in the ProgramData directory with the following ACLs

```C:\ProgramData\BlueStacks_nxt\ Everyone:(OI)(CI)(F)
                               NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
                               BUILTIN\Administrators:(I)(OI)(CI)(F)
                               CREATOR OWNER:(I)(OI)(CI)(IO)(F)
                               BUILTIN\Users:(I)(OI)(CI)(RX)
                               BUILTIN\Users:(I)(CI)(WD,AD,WEA,WA)

Successfully processed 1 files; Failed processing 0 files
```

The (F) permission assigned to Everyone means that all users can fully access and modify the contents.
This allows modifying both the virtual drives (storage used by emulators) and their Virtual Box config files.
Editing the former gives the attacker an opportunity to add automatically executed code to the underlying virtual
machine, creating a backdoor which will run whenever a legitimate user starts the emulator. Editing the latter
allows reconfiguring shared directory settings to include the entire C drive, allowing the code to escape from
Virtual Box into the host operating system.

To enable a virtual machine escape, the attacker would modify the file
```C:\ProgramData\BlueStacks_nxt\Engine\Nougat32\Nougat32.bstk``` (or a similar file for specific virtual
machine used by the Bluestacks version of the victim; different BlueStacks versions can use other Android VMs)
and modify it to change the line
```
        <SharedFolder name="BstSharedFolder" hostPath="C:\ProgramData\BlueStacks_nxt\Engine\UserData\SharedFolder" writable="true" autoMount="false"/>
```
to
```
        <SharedFolder name="BstSharedFolder" hostPath="C:\" writable="true" autoMount="false"/>
```
which will allow full access to the Windows filesystem (with restrictions depending on the access level of user
running BlueStacks) through ```/mnt/windows/BstSharedFolder```.

After configuring shared folders to enable VM escape, the attacker needs to modify the virtual drive's filesystem
to add code that will be executed when run by the privileged user. There are multiple ways of doing this, but
the most straightofrward one demonstrated in the PoC is by installing an application which starts automatically
through the use of ```BOOT_COMPLETED``` broadcast receiver.

Final step of the exploitation is performing the escape. With access to the host OS filesystem, it can be achieved
by adding an executable file to current user's ```AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup```.
While the application has no way of knowing who the current user is, it can simply enumerate the subdirectories
in ```C:\Users``` and attempt writing to all of them.
 
**Reproduction**

1. Set up attacker and victim accounts, preferably making attacker unprivileged and victim the administrator
2. Victim: install the vulnerbale version of BlueStacks
3. Attacker: modify Nougat32.bstk to give Android access to C drive
4. Attacker: run the Android system and install a malicious application on it
5. Victim: run BlueStacks, causing the malicious application to drop payload in your startup directory
6. Victim: reboot the machine and log into your account again
7. Startup payload should be executed with your privileges

**Remedy**

Install a newer version of BlueStacks.
