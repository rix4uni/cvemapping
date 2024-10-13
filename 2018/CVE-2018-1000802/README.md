# Python CVE-2018-1000802 Proof-of-Concept

This is a PoC for the vulnerability in `make_archive` function exported by `shutil` builtin module.

Vulnerability is present in CPython (Python) 2.7 prior to commit add531a1e55b0a739b0f42582f1c9747e5649ace.

For the vulnerability to be exploitable in the wild there are several conditions:
1.	Code must run on Windows machine;
2.	There must be a zip utility accessible via command line e.g. Zip for Windows;
3.	Import zipfile must fail.

Please see poc.py for code examples.
