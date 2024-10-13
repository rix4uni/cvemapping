**CVEID**: CVE-2019-14326

**Name of the affected product(s) and version(s)**: Andy (all versions up to 46.11.113)

**Problem type**: CWE-284: Improper Access Control

---

**Summary**

Andy is an Android emulator for Windows and Mac.

During our tests, we have found open local TCP ports which could be exploited to escalate privileges from user to root.
All versions of Andy (up to and including 46.11.113, and possibly newer versions as well) allow telnet and ssh access
to root account without password protection.
 
**Description**
 
Andy emulator opens ports 22 and 23 inside the emulated Android systems. These are ssh and telnet ports, giving access
to the root shell with no password protection. While the issue is not exploitable remotely because the emulated Android
device is only visible inside a VMWare network accessible only to the host operating system and the emulated Android
system itself, it can be used by malicious apps installed inside the emulated systems to escalate privileges to root
without user interaction.
 
**Reproduction**
 
```echo "[command_to_execute]" | busybox telnet localhost 23```
 
**Mitigation**

Kill telnet and ssh daemons.
