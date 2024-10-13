# CVE-2019-17662
## Python implementation of CVE-2019-17662 TinyVNC Arbitrary File Read leading to Authentication Bypass Exploit
### Based on the original EDB PoC by Nikhith Tumamlapalli ([EDB ID: 47519](https://www.exploit-db.com/exploits/47519))

Original PoC exploit does not work due to path normalisation in the Python Requests library. The code in this repository fixes and improves the original exploit.

Exploit is mostly automatic. See `./CVE-2019-17662.py --help` for full range of switches

**Warning:** The code in this repository may be used for academic/ethical purposes only. The author does not condone the use of this exploit for any other purposes -- it may only be used against systems which you own, or have been granted access to test.
