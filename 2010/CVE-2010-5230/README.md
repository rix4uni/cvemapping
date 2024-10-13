# CVE-2010-5230
Multiple untrusted search path vulnerabilities in MicroStation 7.1 allow local users to gain privileges via a Trojan horse (1) mptools.dll, (2) baseman.dll, (3) wintab32.dll, or (4) wintab.dll file in the current working directory, as demonstrated by a directory that contains a .hln or .rdl file. NOTE: some of these details are obtained from third party information.

Hi folks,

After playing with windows DLL hijack toolkit,I got exploit POC for Pipe
design software Bentaly Microstation 7.1,Nero 8.2.8.0,Quicktime pictureviwer
7.6.5

 Bentley Microstation 7.1:

File :Ustation.exe  File type:hln  Hijack Dll:mptools.dll
File :Ustation.exe  File type:rdl   Hijack
Dll:baseman.dll,wintab32.dll,wintab.dll

Nero 8.2.8.0

File :nero.exe  File type:nab Hijack Dll:bcgpoleacc.dll

Quicktime pictureviwer 7.6.5

File :pictureviewer.exe   File type:mac,pct,pic,pict,pnt,pntg,qti,qtif
Hijack Dll:cfnetwork.dll
File :pictureviewer.exe   File type:pct,pic,pict,pnt,pntg,qti,qtif
Hijack Dll:corefoundation.dll

Download Link Generated POC's

https://paper.seebug.org/papers/old_sebug_paper/Exploits-Archives/2010-exploits/1008-exploits/Microstation_dllhijact_exploit.rar

https://paper.seebug.org/papers/old_sebug_paper/Exploits-Archives/2010-exploits/1008-exploits/Nero_dllhijack_exploit.rar

https://paper.seebug.org/papers/old_sebug_paper/Exploits-Archives/2010-exploits/1008-exploits/quicktime_pictureviwer_dllhijact_exploit.rar


For test cases-
http://reach2kalyan.blogspot.com/2010/08/playing-with-dll-hijack-bug.html


Kalyan
http://reach2kalyan.blogspot.com/
