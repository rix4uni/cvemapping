# CVE-2022-27438
> Caphyon Ltd Advanced Installer 19.3 "CustomDetection" Update Check Remote Code Execution Vulnerability.

Usage: `python3 cve-2022-27438_poc.py`

Details in the report at [gerr.re](https://gerr.re/posts/cve-2022-27438/).

## Steps to reproduce
For other affected products, you have to change the update server and update configuration filename. These can often be found in the updater `.ini` in the application installation directory.

1. Install [Advanced Installer 19.3](https://www.advancedinstaller.com/downloads/advinst.msi);
2. Set spoof `www.advancedinstaller.com` to our attacker ip;
    * For the proof of concept it is easiest to edit `c:\windows\system32\drivers\etc\hosts` on the target.
        - Attackers may e.g. use:
            + poorly configured routers/switches/DNS
            + DNS spoof / cache poisoning
            + ARP spoof / cache poisoning
3. Generate self-signed certificates;
   * e.g. using `openssl req -new -x509 -keyout www.advancedinstaller.com.pem -out www.advancedinstaller.com.pem -days 365 -nodes -subj "/CN=www.advancedinstaller.com"`
4. Run the proof of concept script on the attacker;
5. Start Advanced Installer to trigger update automatically, or
    * wait for 2 days to trigger update automatically, or
    * trigger update manually through the application menu/settings, or
    * trigger update manually by starting the update application at `C:\Program Files (x86)\Caphyon\Advanced Installer 19.3\bin\x86\updater.exe`;
6. Proceed with the Windows untrusted certificate security alert (if applicable).

As a result, the binary specified in `CustomDetection` with parameters specified in `CustomDetectionParameters` is executed in the context of the current user.

