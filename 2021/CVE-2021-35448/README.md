# CVE-2021-35448

**Description:** Local Privilege Escalation in Remote Mouse 3.008

**Vulnerable App:** [Download](https://www.exploit-db.com/apps/4e06b0e24ad2dbf6fde0da11b77dd98d-RemoteMouse.exe)

**Exploit-DB:** [https://www.exploit-db.com/exploits/50047](https://www.exploit-db.com/exploits/50047)

**Proof Of Concept:**

- Open Remote Mouse from taskbar
- Go to Settings -> Image Transfer Folder
- Click "Change...", a Save As dialog box will appear
- Enter `C:\Windows\System32\cmd.exe` 
- Command Prompt will be opened with admin privileges

**Screenshots:**

![](https://i.imgur.com/vHacNUg.png)

![](https://i.imgur.com/i5csLKg.png)

![](https://i.imgur.com/9uh9atb.png)

![](https://i.imgur.com/eEb9y8u.png)

![](https://i.imgur.com/DfxaLEU.png)