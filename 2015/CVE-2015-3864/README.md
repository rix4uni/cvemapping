## SCAREDYCAT! version 0.1 beta

Python script to generate a malicious MP4 file 
and start a web server hosting a page with the
embedded 'video' file on port 8080.

This exploits another Stagefright vulnerability,
the integer overflow vulnerability (CVE-2015-3864),
published by Exodus Intelligence.

### author: vvn (eudemonics) <root [at] nobody [dot] ninja>
### built upon original exploit code from Google for CVE-2015-3864

####** usage: scaredycat.py [-h] [-p PAYLOAD] [-v] [libcfile]

optional arguments:

    libcfile              path to libc.so file (usually in /system/lib on
                          android devices). one is included in the repo.
    -h, --help            show this help message and exit
    -p PAYLOAD, --payload PAYLOAD
                          path to shellcode/payload to be injected into mp4 file.
                          a generic one created by meterpreter is included.
    -v, --version         version information
