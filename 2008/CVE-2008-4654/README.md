# VLC-CVE-2008-4654-Exploit
Well, it's just an old vulnerability whose CVE number is CVE-2008-4654. This vulnerability is caused by Out of Memory at line 1650 of modules/demux/ty.c.
```
stream_Read(p_demux->s, mst_buf, 8 + i_map_size);
```
When I downloaded the EXP from other websites, I found that it doesn't work correctly on my Windows 7 Ultimate x64. So I change the return address from 0x68f0cfad to 0x6a314b52, then it works!

Old:
```
0x68f0cfad : jmp esp 
{PAGE_EXECUTE_READ} [libqt4_plugin.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False
```

After I found this module doesn't exist, I changed into:
```
0x6a314b52 : push esp # ret
{PAGE_EXECUTE_READ} [libvlc.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False
```

It works on VLC 0.9.4. Have fun!
