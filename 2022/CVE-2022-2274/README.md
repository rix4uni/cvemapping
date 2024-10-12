# OpenSSL-src Heap Memory Corruption with RSA Private Key Operation : CVE-2022-2274

# Summary

[OpenSSL-src-rust](https://github.com/alexcrichton/openssl-src-rs) is a source code and logic to build OpenSSL from source written in rust and packaged as a crate. There are currently two maintained branches, matching the two [maintained OpenSSL versions](https://www.openssl.org/policies/releasestrat.html) which are `main` which builds OpenSSL 3.0 and `release/111` which builds OpenSSL 1.1.1.

The OpenSSL 3.0.4 release introduced a serious bug in the RSA implementation for X86_64 CPUs supporting the AVX512IFMA instructions. This issue makes the RSA implementation with 2048 bit private keys incorrect on such machines and memory corruption will happen during the computation. As a consequence of the memory corruption an attacker may be able to trigger a remote code execution on the machine performing the computation. SSL/TLS servers or other servers using 2048 bit RSA private keys running on machines supporting AVX512IFMA instructions of the X86_64 architecture are affected by this issue.

This vulnerability made building OpenSSL version 3.0 using [openssl-src-rust](https://github.com/alexcrichton/openssl-src-rs) to fail and crash in the process on the machine supporting AVX512IFMA instructions of the X86_64 architecture.

# Product

**openssl-src**([Rust](https://github.com/advisories?query=ecosystem%3Arust))

# Tested Version

**>= 300.0.8, < 300.0.9**

# Details
## Issue: openssl-src 300.0.8 heap memory corruption with RSA private key operation `(GHSA-735f-pg76-fxc4)`

The processes to reproduce the error or crash are as follow:

Build OpenSSL-3.0.4 on a CPU with AVX512 (this demonstration uses a Core i7-1065G7) with:

    CFLAGS="-O3 -g -fsanitize=address" ./config
    make

Run a test:

    make V=1 TESTS=test_exp test

The sanitizer complains:

    ==481618==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60c000089400 at pc 0x7f01e32a9509 bp 0x7fff643ec100 sp 0x7fff643ec0f8
    READ of size 8 at 0x60c000089400 thread T0
        #0 0x7f01e32a9508 in bn_select_words crypto/bn/rsaz_exp.h:64
        #1 0x7f01e32a9508 in bn_reduce_once_in_place crypto/bn/rsaz_exp.h:74
        #2 0x7f01e32a9508 in ossl_rsaz_mod_exp_avx512_x2 crypto/bn/rsaz_exp_x2.c:223
        #3 0x7f01e3287dc8 in BN_mod_exp_mont_consttime_x2 crypto/bn/bn_exp.c:1448
        #4 0x4042c3 in test_mod_exp_x2 test/exptest.c:260
        #5 0x40611a in run_tests test/testutil/driver.c:370
        #6 0x4039ba in main test/testutil/main.c:30
        #7 0x7f01e2c29319 in __libc_start_call_main (/usr/lib/libc.so.6+0x29319)
        #8 0x7f01e2c293e4 in __libc_start_main_impl (/usr/lib/libc.so.6+0x293e4)
        #9 0x403c40 in _start (/home/xry111/sources/lfs/openssl-3.0.4/test/exptest+0x403c40)
    
    0x60c000089400 is located 0 bytes to the right of 128-byte region [0x60c000089380,0x60c000089400)
    allocated by thread T0 here:
        #0 0x7f01e3ae5107 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:69
        #1 0x7f01e34aa7a8 in CRYPTO_zalloc crypto/mem.c:197
    
    SUMMARY: AddressSanitizer: heap-buffer-overflow crypto/bn/rsaz_exp.h:64 in bn_select_words
    Shadow bytes around the buggy address:
      0x0c1880009230: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
      0x0c1880009240: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x0c1880009250: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
      0x0c1880009260: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
      0x0c1880009270: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    =>0x0c1880009280:[fa]fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
      0x0c1880009290: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
      0x0c18800092a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x0c18800092b0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
      0x0c18800092c0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
      0x0c18800092d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
    ==481618==ABORTING

It has been proposed by the discoverer of the issue that previous [commits](https://github.com/openssl/openssl/pull/18510/commits) to the OpenSSL code might have introduced the bug. The commit was to fix `BN_mod_exp_consttime` so it does not produce unreduced result. The `bn_reduce_once_in_place` function caused the heap memory corruption. 

[crypto/bn/rsaz_exp_x2.c](https://github.com/openssl/openssl/pull/18510/files#diff-854689acd04b8f1b65120880bebcd98d519e89b601328820f276ec0e5c164c4f)

    @@ -220,6 +220,9 @@ int ossl_rsaz_mod_exp_avx512_x2(BN_ULONG *res1,
        from_words52(res1, factor_size, rr1_red);
        from_words52(res2, factor_size, rr2_red);
    
        bn_reduce_once_in_place(res1, /*carry=*/0, m1, storage, factor_size);
        bn_reduce_once_in_place(res2, /*carry=*/0, m2, storage, factor_size);

This was fixed with an update found in this [commit](https://github.com/openssl/openssl/pull/18626/commits) which stated that `bn_reduce_once_in_place` expects the number of `BN_ULONG`, but `factor_size` is moduli bit size. This update was included in the OpenSSL 3.0.5 released in October 12, 2022.

[crypto/bn/rsaz_exp_x2.c](https://github.com/openssl/openssl/pull/18626/files#diff-854689acd04b8f1b65120880bebcd98d519e89b601328820f276ec0e5c164c4f)

    @@ -257,6 +257,9 @@ int ossl_rsaz_mod_exp_avx512_x2(BN_ULONG *res1,
        from_words52(res1, factor_size, rr1_red);
        from_words52(res2, factor_size, rr2_red);
    
        /* bn_reduce_once_in_place expects number of BN_ULONG, not bit size */
        factor_size /= sizeof(BN_ULONG) * 8;
    
        bn_reduce_once_in_place(res1, /*carry=*/0, m1, storage, factor_size);
        bn_reduce_once_in_place(res2, /*carry=*/0, m2, storage, factor_size);
## Impact

An attacker could theoretically exploit this vulnerability by sending a transmission across a network (e.g., a TCP/IP network). A successful exploit could result to:

- Disrupt services (i.e., DoS);
- Steal information in memory (i.e., confidentiality breach);
- Alter information in memory (i.e., integrity breach);
- Invoke/execute a definable list of specific actions on the target application/host;
- Invoke/execute arbitrary commands/code on the target application/host.
## Patches
- Users of the OpenSSL 3.0.4 version should upgrade to OpenSSL 3.0.5 and above.
- OpenSSL 1.1.1 and 1.0.2 are not affected by this issue.
## Resources
- [https://nvd.nist.gov/vuln/detail/CVE-2022-2274](https://nvd.nist.gov/vuln/detail/CVE-2022-2274)
- [openssl/openssl#18625](https://github.com/openssl/openssl/issues/18625)
- [https://git.openssl.org/gitweb/?p=openssl.git;a=commitdiff;h=4d8a88c134df634ba610ff8db1eb8478ac5fd345](https://git.openssl.org/gitweb/?p=openssl.git;a=commitdiff;h=4d8a88c134df634ba610ff8db1eb8478ac5fd345)
- [https://rustsec.org/advisories/RUSTSEC-2022-0033.html](https://rustsec.org/advisories/RUSTSEC-2022-0033.html)
- [https://www.openssl.org/news/secadv/20220705.txt](https://www.openssl.org/news/secadv/20220705.txt)
- [https://security.netapp.com/advisory/ntap-20220715-0010/](https://security.netapp.com/advisory/ntap-20220715-0010/)
## CVSS Based Metrics
| Severity            | Critical 9.8 / 10 |
| ------------------- | ----------------- |
| Attack vector       | Network           |
| Attack complexity   | Low               |
| Privileges required | None              |
| User interaction    | None              |
| Scope               | Unchanged         |
| Confidentiality     | High              |
| Integrity           | High              |
| Availability        | High              |

# CVE
- CVE-2022-2274
# Credits
- This issue was reported to OpenSSL on 22nd June 2022 by [Xi Ruoyao](https://github.com/xry111). The fix was developed by [Xi Ruoyao](https://github.com/xry111).
- This issue was discovered and reported by GHSL team member [Konrad Borowski](https://github.com/xfix)**.**

