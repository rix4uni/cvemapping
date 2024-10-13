# Exploiting CVE-2016-2334 7zip HFS+ vulnerability
`hfsGenerator.py`
> Script used to generate HFS+ file

`heap.js`
> WinDbg js script.

After loading script, setup allocation hook in the following way:

> bp ntdll!RtlAllocateHeap "pt \"dx Debugger.State.Scripts.heap.Contents.handleRtlHeapAlloc();g\""

Next you can list heap chunks with information about allocated there object :
```
0:000> !heap -x 0x003a9bb0  
Entry     User      Heap      Segment       Size  PrevSize  Unused    Flags
-----------------------------------------------------------------------------
003a9ba8  003a9bb0  00340000  00340000     10028        d8        18  busy extra fill 		

0:000> dx Debugger.State.Scripts.heap.Contents.showHeap("00340000")

004e9bc0 2005 001b  [00]   004e9bc8    10010 - (busy) - 05 7z!CBuffer<unsigned char>::CBuffer<unsigned char>
004f9be8 7c1a 2005  [00]   004f9bf0    3e0c8 - (free)
00537cb8 0011 7c1a  [00]   00537cc0    00070 - (busy) - 05 7z!CObjectVector<NArchive::NHfs::CItem>::AddNew
00537d40 0011 0011  [00]   00537d48    00070 - (busy) - 05 7z!CObjectVector<NArchive::NHfs::CItem>::AddNew
00537dc8 0006 0011  [00]   00537dd0    00016 - (busy) - 05 7z!UString::ReAlloc2
00537df8 0011 0006  [00]   00537e00    00070 - (busy) - 05 7z!CObjectVector<NArchive::NHfs::CItem>::AddNew
00537e80 000b 0011  [00]   00537e88    0003c - (busy) - 05 7z!UString::ReAlloc2
00537ed8 0011 000b  [00]   00537ee0    00070 - (busy) - 05 7z!CObjectVector<NArchive::NHfs::CItem>::AddNew
00537f60 0006 0011  [00]   00537f68    00012 - (busy) - 05 7z!UString::ReAlloc2
00537f90 0011 0006  [00]   00537f98    00070 - (busy) - 05 7z!CObjectVector<NArchive::NHfs::CItem>::AddNew
00538018 0004 0011  [00]   00538020    00008 - (busy) - 05 7z!CRecordVector<NArchive::NCramfs::CItem>::ReserveOnePosition

```

Looking just for an allocated objects with vftable ? No problem:

```
0:000> Debugger.State.Scripts.heap.Contents.showObjects("00480000")

        00538830 0007 000b  [00]   00538838    00020 - (busy)          7z_exe!COutFileStream::`vftable'
 # 
00 ntdll!RtlAllocateHeap
01 ntdll!RtlpAllocateHeap
02 ntdll!RtlAllocateHeap
WARNING: Stack unwind information not available. Following frames may be wrong.
03 MSVCR120!malloc
04 7z_exe!operator new
05 7z_exe!CArchiveExtractCallback::GetStream
06 7z!NArchive::NHfs::CHandler::Extract
07 7z_exe!DecompressArchive
08 7z_exe!Extract
09 7z_exe!Main2
0a 7z_exe!main
0b 7z_exe!__tmainCRTStartup
0c kernel32!BaseThreadInitThunk
0d ntdll!__RtlUserThreadStart
0e ntdll!_RtlUserThreadStart

===============================================================
        005388e8 0009 000e  [00]   005388f0    00030 - (busy)          7z!CExtentsStream::`vftable'
 # 
00 ntdll!RtlAllocateHeap
01 ntdll!RtlpAllocateHeap
02 ntdll!RtlAllocateHeap
WARNING: Stack unwind information not available. Following frames may be wrong.
03 MSVCR120!malloc
04 7z!operator new
05 7z!NArchive::NHfs::CHandler::GetForkStream
06 7z!NArchive::NHfs::CHandler::ExtractZlibFile
07 7z!NArchive::NHfs::CHandler::Extract
08 7z_exe!DecompressArchive
09 7z_exe!Extract
0a 7z_exe!Main2
0b 7z_exe!main
0c 7z_exe!__tmainCRTStartup
0d kernel32!BaseThreadInitThunk
0e ntdll!__RtlUserThreadStart
0f ntdll!_RtlUserThreadStart

```