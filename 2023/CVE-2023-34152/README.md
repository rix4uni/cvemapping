# CVE-2023-34152
RCE vulnerability affecting ImageMagick 6.9.6-4. This vulnerability allows the attacker to execute commands on the victim system. Thus, allowing for Remote Command Execution.

This is a POC which was inspired by fullwaywang discovery of CVE-2023-34152.

[Vulnerability Disclosure](https://github.com/ImageMagick/ImageMagick/issues/6339)

```
Usage: python3 CVE-2023-34152.py Attacker_IP Attacker_Port
```
## Description
an aribitary code execution vulnerability (shell command injection) in OpenBlob, which is actually an incomplete fix to CVE-2016-5118.

CVE-2016-5118 showed that opening any image file whose name starts with a '|' character, ImageMagick will popen the remaining part of the file name. As a fix, it add a configure option --enable-pipes to specially turn on the support of pipes; and also, the invocation of SanitizeString is added before popen_utf8 the filename to suppress aribitary command execution.

However, SanitizeString only filters out characters like single quotes but not ` or ". This allows shell command injection through malformed file name.

Credits: [fullwaywang](https://github.com/fullwaywang)
## PATCH

Upgrade to version 7.1.1.10 

---