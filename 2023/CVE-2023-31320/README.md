<h1 align="center">CVE-2023-31320</h1>

Proof of concept code for a denial of service vulnerability in the AMD display driver that corrupts the display.

[AMD security bulletin](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-6003.html)

## Demo

_**This video contains flashing lights!**_

https://github.com/whypet/CVE-2023-31320/assets/47226783/658776cb-6dbc-4a76-a671-fc1f4924b2a9

## Building

- Clang: `clang++ main.cpp -Oz -luser32 -ld3d11 -ld3dcompiler -o out/CVE-2023-31320.exe`
- GCC: `g++ main.cpp -Oz -municode -luser32 -ld3d11 -ld3dcompiler -o out/CVE-2023-31320.exe`
- MSVC++: `cl main.cpp /O1 /Foout/ /link user32.lib d3d11.lib d3dcompiler.lib /out:out/CVE-2023-31320.exe`
