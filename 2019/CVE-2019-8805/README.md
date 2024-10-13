# CVE-2019-8805
Exploit for CVE-2019-8805 Apple EndpointSecurity framework Privilege Escalation

A validation issue existed in the entitlement verification. This issue was addressed with improved validation of the process entitlement. This issue is fixed in macOS Catalina 10.15.1. An application may be able to execute arbitrary code with system privileges.

# Compile and Execute

- Compile
```
gcc -framework Foundation appleEPSPrivEsc.m -o appleEPSPrivEsc
```
- Execute
```
./appleEPSPrivEsc
```

![image](https://github.com/user-attachments/assets/a145a515-ae05-4cb4-91e2-b7da69037a22)

