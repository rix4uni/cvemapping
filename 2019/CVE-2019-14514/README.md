**CVEID**: CVE-2019-14514

**Name of the affected product(s) and version(s)**: Microvirt MEmu (all versions prior to 7.0.2)

**Problem type**: CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')

---

**Summary**

MEmu is an Android emulator for Windows. During our tests, we have found an open TCP port which could be exploited to gain code execution with root privileges.
All Microvirt MEmu versions prior to 7.0.2 feature a vulnerable binary which listens on port 21509. An attacker could gain remote code execution with root privileges on an emulated Android system by sending crafted messages containing special characters used as command delimiters in Unix shells.
 
**Description**
 
```/system/bin/systemd``` binary (not related to Freedesktop systemd init system) is run by the root user and listens for commands on port 21509. If a command starting with installer:uninstall is sent, attacker-controlled input will be inserted into a shell command template and passed to /system/bin/sh without verification or escaping. This means that a remote attacker could insert special characters like ```;```, ```&&``` or ```||``` to send his own shell commands which will be executed on the emulated system with root privileges.
 
**Reproduction**
 
```echo "installer:uninstall;[shell_command_to_execute]" | nc [emulator_ip] 21509```
 
The emulator should execute the command and then reboot.
 
**Remedy**

Update MEmu to version 7.0.2 or later.
