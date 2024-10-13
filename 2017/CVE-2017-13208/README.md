# CVE-2017-13208-Scanner
https://nvd.nist.gov/vuln/detail/CVE-2017-13208
## Introduction
This is a simple script capable of detecting the CVE-2017-13208 vulnerability in Android libnetutils.so files.
## How it works
Using r2pipe, the script checks whether dhcp_size's value is checked, if it isn't - the file is vulnerable.
All of the different libnetutils.so files that were researched compared a fixed number with dhcp_size's value.
Therefore, the script checks for the existence of one of those fixed numbers - 1268, 1260 (0x4ec, 0x4f4), which indicates that
the file isn't vulnerable.
## Usage
./Script.py <file_path>
