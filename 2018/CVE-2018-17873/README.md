# CVE-2018-17873

WiFiRanger indoor routers (Core, GoAC) and their outdoor paired routers (Sky Pro, EliteAC, EliteAC FM) running firmware version 7.0.8rc3 and earlier allow anonymous FTP read/write access and have left the SSH Private Key in the clear - making it a trivial task to view/copy the key and log in with root privileges.

Adjacent network access required to exploit this vulnerability.

# Exploit:
Extremely simple shell script that grabs the private key and logs in as root.

# Usage:
```./wifiRangerPwn.sh <WiFiRanger IP>```
