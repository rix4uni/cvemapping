# ghostscript-CVE-2023-43115
A small write-up with examples to help understand CVE-2023-43115.

> [!WARNING] 
> I wrote this mainly for myself to understand the problem and to learn about cybersecurity. So there may be errors.

## The Problem
To utilize the IJS device (Improved Inkjet Printing), Ghostscript is required to start an IJS server. This is accomplished by using the path specified in the IjsServer parameter. The IjsServer parameter can be configured to reference any desired file within the file system, and Ghostscript subsequently executes that designated file. Here it is easy to see how this could potentially be misused, e.g. you could run the following ghostscript command to print hello world.

```console
❯ gs -sDEVICE=ijs -sIjsServer="bash -c 'echo Hello World>&2'"
GPL Ghostscript 9.55.0 (2021-09-27)
Copyright (C) 2021 Artifex Software, Inc.  All rights reserved.
This software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:
see the file COPYING for details.
Hello World
```
In it self this isn´t that problematic since this parameter has to be supplied by the user. However it is also possible to set this device and the IJsServer parameter inside a postscript script.
See for example `attack_example_*.ps` (execute with `gs FILENAME`). This in turn could allow an attack to execute code on the machine running this script. But, this problem is known and officially [documented](https://ghostscript.com/docs/9.56.1/Devices.htm#IJS) and could be **prevented by setting LockSafetyParams** to true.

To leverage this CVE while LockSafetyParams is enabled, an attacker would need a working exploit to change LockSafetyParams. However, if such an exploit is available, there could be a number of other possible attack vectors depending on the version used.

## The Fix
The author of the [fix](https://git.ghostscript.com/?p=ghostpdl.git;a=commit;h=e59216049cac290fb437a04c4f41ea46826cfba5) Ken Sharp called the mentioned LockSafetyParams security solution hacky because it is implemented in postscript and is thus vulnerable to postscript code. This led to several security issues in the past where it was possible to overwrite this parameter (for an example see [CVE-2018-19475 writeup](https://securitylab.github.com/research/ghostscript-CVE-2018-19475/)
). The fix **changes the protection mechanism** that prevents setting the IjsServer path from LockSaftyParams **to** the new **-dSAFER** parameter, which cannot be affected by postscript code.

> [!NOTE] 
> The [Documentation](https://ghostscript.com/docs/9.55.0/Devices.htm#IJS) of the vulnerable version 9.55.0 allready states to use the -dSAFER parameter which seems to be a documentation error.

## Sources and further reading
- [CVE-2023-43115](https://nvd.nist.gov/vuln/detail/CVE-2023-43115)
- [Fix commit](https://git.ghostscript.com/?p=ghostpdl.git;a=commit;h=e59216049cac290fb437a04c4f41ea46826cfba5)
- [CVE-2018-19475 writeup](https://securitylab.github.com/research/ghostscript-CVE-2018-19475/)
- [IJS DOC](https://ghostscript.com/docs/9.56.1/Devices.htm#IJS)
- [LockSaftyParams DOC](https://ghostscript.com/docs/9.55.0/Language.htm#LockSafetyParams)

