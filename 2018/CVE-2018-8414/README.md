# CVE-2018-8414 POC

Windows Shell Package Setting Remote Code Execution Vulnerability

Since : Windows 10 Version 1703 to 1803
       / Windows Server Version 1709 to 1803
       
Note : Some time the exploit fail depending of the file location (default policy settings), so for that just copy the file in the Package Settings Dir and it should execute rightly
* C:\Users\\[USER]\AppData\Local\Packages\windows.immersivecontrolpanel_cw5n1h2txyewy\LocalState\Indexed\Settings\\[LANGUAGE]\

More details : https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2018-8414

Credit to 0patch
