## CVE-2018-1000117
-----------

Python Software Foundation CPython version From 3.2 until 3.6.4 on Windows contains a Buffer Overflow vulnerability in os.symlink() function on Windows that can result in Arbitrary code execution, likely escalation of privilege. This attack appears to be exploitable via a python script that creates a symlink with an attacker controlled name or location. This vulnerability appears to have been fixed in 3.7.0 and 3.6.5.

-----------
## Vulnerable Versions

    Python 2.7
    Python 3.4
    Python 3.5
    Python 3.6

------------
## Credits
* Alexey Izbyshev (Reporter) - ![GitHub](https://assets-cdn.github.com/favicon.ico) [Alexey Izbyshev](https://github.com/izbyshev)
* 1337r00t (Exploiter) - ![Twitter](https://abs.twimg.com/favicons/favicon.ico) [1337r00t](https://twitter.com/_1337r00t)
