# ADSelfService-Plus-PoC CVE-2019-12476
ADSelfService Plus version 4.3.3  PoC for an authentication bypass on Windows 10. 

Affects all versions of Windows 

PoC Video

[![](http://img.youtube.com/vi/4e1HTIYOWVQ/0.jpg)](http://www.youtube.com/watch?v=4e1HTIYOWVQ "")

Steps to repoduce 

1. Disconnect from your enterprise network 
2. Connect to your own hotspot 
3. Click on reset password; the thick client browser should error out with a 404 if the password reset web application is hosted in the intranet 
4. Click on search for this site which should open a new internet explorer window. 
5. Press Ctrl S to open file explorer and browse to c:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe 
6. Get System Shell without any authentication required. 

### Fix 

Update to the latest version; current latest version is 5.0.6


### Notes 
The same exploit was verified to work in another vendor, so give it a shot if you're using a self service password reset app in your organazation. 

I was able to bypass the patch 5.0.6 but it's very unstable once I find a stable way of automatating the exploit it will be released.  

### Thanks To
[scottjw](https://github.com/scottjw) - For automating the exploit. 
