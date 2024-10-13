Samba versions 2.2.0 to 2.2.8
==============================

This exploits the buffer overflow found in Samba versions
2.2.0 to 2.2.8. This particular module is capable of
exploiting the flaw on x86 Linux systems that do not
have the noexec stack option set.
NOTE: Some older versions of RedHat do not seem to be vulnerable
since they apparently do not allow anonymous access to IPC.

CVE
===

- CVE-2003-0201
- OSVDB-4469
- BID-7294

Compile
=======

gcc trans2open.c -o trans2open

Metasploit
==========

https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/linux/samba/trans2open.rb

