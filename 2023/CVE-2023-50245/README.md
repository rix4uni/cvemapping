# CVE-2023-50245



## 취약점 개요

- CVE-2023-50245

- CVSS : 9.8

- Dec 11, 2023

- Image Viewer Vulnerability



## 취약점 설명

[github advisories](https://github.com/afichet/openexr-viewer/security/advisories/GHSA-99jg-r3f4-rpxj)

arbitrary address write vulnerability

**[ POC 1 ]**

```
(1404.9264): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
openexr_viewer+0x27be4:
00007ff713ff7be4 c744880c0000803f mov     dword ptr [rax+rcx*4+0Ch],3F800000h ds:0000029cb371600c=????????
```

*Attempt to write the value 1.0 to the memory address 0x29CB371600C*


**[ POC 2 ]**

```
(8660.7e44): Access violation - code c0000005 (!!! second chance !!!)
openexr_viewer+0x27be4:
00007ff713ff7be4 c744880c0000803f mov     dword ptr [rax+rcx*4+0Ch],3F800000h ds:0000020a3ac8000c=????????
```

*Attempt to write the value 1.0 to the memory address 0x20A3AC8000C*

[target : openexr-viewer](https://github.com/afichet/openexr-viewer)