# CVE-2024-55503
Termius App MacOS dylib Command injection

# Description
An issue in termius before v.9.9.0 allows a local attacker to execute arbitrary code via a crafted script to the DYLD_INSERT_LIBRARIES component. using dylib
```shell
DYLD_INSERT_LIBRARIES=exploit_combined.dylib /Applications/Termius.app/Contents/MacOS/Termius
```
# Preduce

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/R-Kze6liCwA/maxresdefault.jpg)](https://youtu.be/R-Kze6liCwA)

# Impact
command execution (local)

# References
CVE Record: https://www.cve.org/CVERecord?id=CVE-2024-55503
