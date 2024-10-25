# CVE-2024-4956

This repository contains a Python utility for automating the exploitation of `CVE-2024-4956` and is capable of mass testing file paths from an input file while automating the process of saving existing file path contents to disk for analysis. Details for the vulnerability can be found [here](https://nvd.nist.gov/vuln/detail/CVE-2024-4956).

## Usage

```
usage: cve-2024-4956.py [-h] [-f FILE] [-p PROXY] [-u URL]

CVE-2024-4956 Path Traversal Exploit Script

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the text file containing a list of file paths to test
  -p PROXY, --proxy PROXY
                        Enable/disable the use of Burp proxy (default: False)
  -u URL, --url URL     Base URL of the target server
```

## Shiro1Extractor

A script for automating the extraction of Apache Shiro 1 hashes from OrientDB .pcl files is available [here](https://github.com/fin3ss3g0d/Shiro1Extractor) for extracting/gathering hashes to use with the Hashcat module.

## Hashcat Module

I have developed a custom Apache Shiro 1 hashcat module while the official project is still lacking support for the algorithm. It is available at my hashcat fork [here](https://github.com/fin3ss3g0d/hashcat). You can take the hashes extracted using this program and use them directly with the module. Here are the steps to use it:

1. Clone the [repository](https://github.com/fin3ss3g0d/hashcat)
2. Build it from source
3. Module is accessible using mode `12150`

I have submitted a [pull request](https://github.com/hashcat/hashcat/pull/4017) to the official Hashcat project, hopefully it will get merged and the module will be available via the official Hashcat repository! A blog was created for the creation of the Hashcat module and is available [here](https://fin3ss3g0d.net/index.php/2024/06/24/crack-faster-hack-smarter-custom-hashcat-module-for-apache-shiro-1-sha-512/).

## Shiro1Tools

[This repository](https://github.com/fin3ss3g0d/Shiro1Tools) contains useful tools that were used when creating the Hashcat module for Apache Shiro 1 such as a standalone `C` program that cracks Apache Shiro 1 hashes using OpenSSL and a `Java` application for generating Apache Shiro 1 hashes.

## Disclaimer

This program is intended for legitimate and authorized purposes only. The author holds no responsibility or liability for misuse of this project.