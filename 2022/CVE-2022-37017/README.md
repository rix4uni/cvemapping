# CVE-2022-37017
Authentication bypass for Symantec Endpoint Protection 14.3.5351 Client User Interface Password 

Symantec Endpoint Protection allows setting a password protection on its UI to prevent configuration changes.
This password check in implemented by logic that is neither in a Protected Process Light (PPL) nor a kernel driver; changing a return value in memory or patching the binary allows an attacker to bypass the password.
This works even if Tamper Protection is enabled. 

If the attacker can execute code with admin privileges, they can import malicious policy XML and/or connection settings for central SEP management.
With this they practically gain full control over the client.
Using the policy import, they can add exclusions, unlock UI options, disable or change the admin password, permanently disable protection, and/or uninstall the client.

If the attacker does not have admin privileges, it can be used to export troubleshooting information, read logs, and view client settings.
On 14.0 the policy can be exported and tamper protection can be disabled without admin permissions. This was not possible in 14.3.5413.3000 .


in 14.3.5351 the following checks if the password matches:

```
.text:00438021 loc_438021:                             ; CODE XREF: sub_437FA0+73↑j
.text:00438021                 mov     ecx, offset ServiceName ; "SepMasterService"
.text:00438026                 call    sub_43DDF0
.text:0043802B                 test    eax, eax
.text:0043802D                 jnz     short loc_4380A5
.text:0043802F                 push    ecx             ; Src
.text:00438030                 lea     eax, [ebp+var_14]
.text:00438033                 mov     ecx, esp
.text:00438035                 push    eax
.text:00438036                 call    ds:??0?$CStringT@_WV?$StrTraitMFC_DLL@_WV?$ChTraitsCRT@_W@ATL@@@@@ATL@@QAE@ABV01@@Z ; ATL::CStringT<wchar_t,StrTraitMFC_DLL<wchar_t,ATL::ChTraitsCRT<wchar_t>>>::CStringT<wchar_t,StrTraitMFC_DLL<wchar_t,ATL::ChTraitsCRT<wchar_t>>>(ATL::CStringT<wchar_t,StrTraitMFC_DLL<wchar_t,ATL::ChTraitsCRT<wchar_t>>> const &)
.text:0043803C                 call    sub_4380F0
.text:00438041                 test    al, al
.text:00438043                 jz      short loc_43804F
.text:00438045                 mov     ecx, esi
.text:00438047                 call    ds:__imp_?OnOK@CDialog@@MAEXXZ ; CDialog::OnOK(void)
.text:0043804D                 jmp     short loc_4380AD
```

The jump that seems to control the success of all password attempts in SymCorpUI.exe is the JZ instruction shown at  .text:00438043.
Changing this to a JNZ (instruction 0x74 -> 0x75) reverses the jump, allowing an arbitrary password to be accepted.

The Python script script finds the install folder for SEP, reads in SymCorpUI.exe, writes a patched copy in the folder next to the script, and runs the patched version in the original working directory.
Run it with privileges, and it will spawn a SEP UI that will accept any incorrect password that is entered.

Now an attacker might export the policy XML under Help -> Troubleshooting. This will contain the configuration including any hashes for the admin password.
The attacker can then edit the XML to change any setting in the client, for example replacing the password hash or disabling the password requirement.
This malicious policy XML can then be imported again using the button next to Export.

The script does some checks to see if it is elevated, if not it forces the patched binary to run without admin privileges.
To run the UI as admin, run the Python script as admin or hardcode the as_admin variable to True.

To avoid having to store specific offsets for each build, the script does a general search/replace for a sequence of instructions that I found to be unique in the three versions I've tested.
It's possible that a different version has multiple matches which might break the PoC. In this case, look through the matches to find a block starting with mov     ecx, offset ServiceName ; "SepMasterService" to find the relevant JZ instruction to patch near the bottom.

For testing the password functionality, one can add the following in the policy XML (at the same level as GlobalGroups) to enable protection.
The hash is an MD5 of the string "test".

```
<AdminPassword ExitNeedPassword="1" UINeedPassword="1" ImportExportNeedPassword="1" UninstallNeedPassword="1">098f6bcd4621d373cade4e832627b4f6</AdminPassword>
```

Symantec responded quickly to the issue, the CVE was registered by them and a fix was published as 14.3 RU6. 

https://support.broadcom.com/external/content/SecurityAdvisories/0/21014
