# Out-Of-Bounds Read in html2xhtml : CVE-2022-44311

# Summary

[Html2xhtml](https://github.com/jfisteus/html2xhtml) v1.3 was discovered to contain an Out-Of-Bounds read in the function static void elm_close(tree_node_t *nodo) at procesador.c. This vulnerability allows attackers to access sensitive files or cause a Denial of Service (DoS) via a crafted html file.

[**CWE-125 Out-of-Bounds Read**](https://cwe.mitre.org/data/definitions/125.html) is a type of software error that can occur when reading data from memory. This can happen if the program tries to read beyond the end of an array, for example. Out of bounds reads can lead to crashes or other unexpected vulnerabilities, and may allow an attacker to read sensitive information that they should not have access to. 

# Product

## html2xhtml

# Tested Version

## 1.3

# Details
## Issue: Out of Bounds Read in `html2xhtml/src/procesador.c`. `(GHSA-28fm-qh2h-3mch)`

Html2xhtml is a command-line tool that converts HTML files to XHTML files. Html2xhtml can generate the XHTML output compliant to one of the following document types: XHTML 1.0 (Transitional, Strict and Frameset), XHTML 1.1, XHTML Basic and XHTML Mobile Profile.

The vulnerability was discovered due to a segfault error that occured when using the `-t frameset` option. A [segmentation fault or segfault](https://stackoverflow.com/questions/2346806/what-is-a-segmentation-fault) is a specific kind of error caused by accessing memory that does not belong to you. It’s a helper mechanism that keeps you from corrupting the memory and introducing hard-to-debug memory bugs.

With the use of [Valgrind](https://valgrind.org/), a tool for finding memory access errors to heap memory (memory that is dynamically allocated with new or malloc) in C and C++ programs, the segfault error was debugged and it reported an `invalid read of size 4` in the test case:


    ==1040381== Memcheck, a memory error detector
    ==1040381== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
    ==1040381== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
    ==1040381== Command: ./src/html2xhtml -t frameset report/vuln/id:000000,sig:11,src:001386+001369,time:12081510,execs:2336913,op:splice,rep:16
    ==1040381== 
    ==1040381== Invalid read of size 4
    ==1040381==    at 0x40E911: elm_close (procesador.c:944)
    ==1040381==    by 0x410617: err_html_struct (procesador.c:1889)
    ==1040381==    by 0x40F20A: err_content_invalid (procesador.c:0)
    ==1040381==    by 0x40F20A: elm_close (procesador.c:959)
    ==1040381==    by 0x40E7C4: saxEndDocument (procesador.c:233)
    ==1040381==    by 0x40DF7A: main (html2xhtml.c:117)
    ==1040381==  Address 0x6f20d4 is not stack'd, malloc'd or (recently) free'd
    ==1040381== 
    ==1040381== 
    ==1040381== Process terminating with default action of signal 11 (SIGSEGV)
    ==1040381==  Access not within mapped region at address 0x6F20D4
    ==1040381==    at 0x40E911: elm_close (procesador.c:944)
    ==1040381==    by 0x410617: err_html_struct (procesador.c:1889)
    ==1040381==    by 0x40F20A: err_content_invalid (procesador.c:0)
    ==1040381==    by 0x40F20A: elm_close (procesador.c:959)
    ==1040381==    by 0x40E7C4: saxEndDocument (procesador.c:233)
    ==1040381==    by 0x40DF7A: main (html2xhtml.c:117)
    ==1040381==  If you believe this happened as a result of a stack
    ==1040381==  overflow in your program's main thread (unlikely but
    ==1040381==  possible), you can try to increase the size of the
    ==1040381==  main thread stack using the --main-stacksize= flag.
    ==1040381==  The main thread stack size used in this run was 8388608.
    ==1040381== 
    ==1040381== HEAP SUMMARY:
    ==1040381==     in use at exit: 88,190 bytes in 13 blocks
    ==1040381==   total heap usage: 22 allocs, 9 frees, 2,218,413 bytes allocated
    ==1040381== 
    ==1040381== LEAK SUMMARY:
    ==1040381==    definitely lost: 0 bytes in 0 blocks
    ==1040381==    indirectly lost: 0 bytes in 0 blocks
    ==1040381==      possibly lost: 0 bytes in 0 blocks
    ==1040381==    still reachable: 88,190 bytes in 13 blocks
    ==1040381==         suppressed: 0 bytes in 0 blocks
    ==1040381== Rerun with --leak-check=full to see details of leaked memory
    ==1040381== 
    ==1040381== For lists of detected and suppressed errors, rerun with: -s
    ==1040381== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
    ==1040419== Memcheck, a memory error detector

The error log from [Valgrind](https://valgrind.org/) led us to the following function where the segfault occured:

[https://github.com/jfisteus/html2xhtml/blob/ffb2f1f12910eb5945413e0bdb9272b508241aa1/src/procesador.c#L940](https://github.com/jfisteus/html2xhtml/blob/ffb2f1f12910eb5945413e0bdb9272b508241aa1/src/procesador.c#L940)

![image](https://user-images.githubusercontent.com/51109125/219993916-a01dfa85-36f4-4e2e-9018-80d5bc3b53ed.png)


It was found that there is a missing type check in the function. The user was passing a node of type `comment` instead of `element` to the function and this results to out of bound read error. A user could provide a malformed document with an invalid `ELM_PTR(nodo).contenttype[doctype]`, resulting in the following comparison in assembly:


    cmp    dword ptr [rbp + rax*4 + 0xc], 4

This vulnerability can be leveraged by attackers to read sensitive files, memory or locations using a doctored file.

## Impact
- This issue can be leveraged by attackers to read sensitive memory, locations or files.
- Attackers can also cause a Denial of Service (DoS) attack via a crafted html file.
## Patches
- This vulnerabilty affects any user using any of the packaged version of the software. There is a fix linked to this [commit](https://github.com/jfisteus/html2xhtml/commit/9523db7834bd677276aa2d1db0ffea16755d6331) in the master branch of the github repository for the software. 
- Users are advised to pull the recent updates to the package dated **October 25, 2022 or later** and compile on their machine. There is no new release or versioning after the bug fix.
## Resources
- [https://nvd.nist.gov/vuln/detail/CVE-2022-44311](https://nvd.nist.gov/vuln/detail/CVE-2022-44311)
- [jfisteus/html2xhtml#19](https://github.com/jfisteus/html2xhtml/issues/19)
- https://securityboulevard.com/2022/06/what-is-an-out-of-bounds-read-and-out-of-bounds-write-error/
- https://cwe.mitre.org/data/definitions/125.html


## CVSS Base Metrics
| Severity      | High 8.1 / 10   |
| ------------------- | --------- |
| Attack complexity   | Low       |
| Privileges required | None      |
| User interaction    | Required  |
| Scope               | Unchanged |
| Confidentiality     | High      |
| Integrity           | None      |
| Availability        | High      |


# CVE
- CVE-2022-44311

# Credits
- This issue was discovered and reported by [@Halcy0nic](https://github.com/Halcy0nic) as an [issue](https://github.com/jfisteus/html2xhtml/issues/19) to the sotfware repository of html2xhtml.


