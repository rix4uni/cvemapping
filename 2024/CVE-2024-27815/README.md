# CVE-2024-27815

XNU kernel buffer overflow. Introduced in `xnu-10002.1.13`, fixed in `xnu-10063.121.3`.

Writeup: https://jprx.io/cve-2024-27815

```bash
gcc TURPENTINE.c -o TURPENTINE
./TURPENTINE
```

### Hash

```bash
$ sha256sum TURPENTINE.c
f7160a6ad7d52f32d64b86cf3006c98a217954d80c3fc71a8f27595e227d0fa0  TURPENTINE.c
```

[Hash posted to X on Feb 17, 2024](https://x.com/0xjprx/status/1758753797441266010)
