## CVE-2011-1237

This is an old POC for CVE-2011-1237 on Windows 7 written in 2013. The
vulnerability was discovered by Tarjei Mandt ([@kernelpool](https://twitter.com/kernelpool))
and explain in his paper [Kernel Attacks through User-Mode Callbacks](https://media.blackhat.com/bh-us-11/Mandt/BH_US_11_Mandt_win32k_WP.pdf).

Several things are hardcoded in this POC and it call the Null page which does
not work anymore. The exploit is describe in my talk
[A Look into the Windows Kernel](https://lse.epita.fr/lse-summer-week-2013/slides/lse-summer-week-2013-26-Bruno%20Pujos-A%20Look%20into%20the%20Windows%20Kernel.pdf).

The only thing the shellcode does is trigger a breakpoint.
