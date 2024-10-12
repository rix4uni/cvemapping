# CVE-2023-42860
Exploit for [CVE-2023-42860](https://nvd.nist.gov/vuln/detail/CVE-2023-4863) (for research purposes only).

This exploit works for versions of macOS earlier to 13.3, even though [Apple´s changelog](https://support.apple.com/en-us/HT213984) says it was fixed in version 14.1.

## Steps
1. [Download](https://mrmacintosh.com/macos-ventura-13-full-installer-database-download-directly-from-apple/) the InstallAssistant.pkg
2. Modify the variable `TARGET_FILE` on the `exploit.sh` file to a SIP protected file on the system (default target is the system TCC database).
3. Run the exploit as **root**:
```sh
$ ./exploit.sh PATH_TO_PKG
```
4. You should now see that the **restricted flag** from the file has been **removed** and be able to modify the SIP protected file directly. Alternatively, you could modify the SIP protected file through `/Applications/Install\ macOS\ Ventura.app/Contents/SharedSupport/SharedSupport.dmg`. The file has to be modified as the **root user**.

## Reference
https://blog.kandji.io/apple-mitigates-vulnerabilities-installer-scripts
