# Invoke-HiveNightmare
PowerShell-based PoC for CVE-2021-36934, which enables a standard user to be able to retrieve the SAM, Security, and Software Registry hives in Windows 10 version 1809 or newer.

# Situation
In specific versions of Windows 10, standard users have read/execute rights to files in [SYSTEMROOT]\System32\Config directory, which is where the Registry hives reside on disk. One can't however, simply navigate to the directory and copy/paste as the hives are loaded and into memory upon system boot and are locked. A standard user can retrieve the hives from Volume Shadow Copies if they exist. 

# Demo
![ Alt text](https://github.com/WiredPulse/Invoke-HiveNightmare/blob/main/PoC.gif) / ! [](name-of-gif-file. gif)

# Disclaimer
The success of this exploit resides on the fact that Volume Shadows Copies exist... without them the code isn't useful. 

# Credits
The vulnerability was discovered by @jonasLyk.
