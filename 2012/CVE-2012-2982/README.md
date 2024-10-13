# CVE-2012-2982

> John Hammond | September 4th, 2021

------------------------


Checking `searchsploit` for Webmin 1.580 I only saw a Metasploit module for
the `/file/show.cgi` Remote Code Execution attack on that legacy Webmin version.

This code is an attempt to recreate that in Python without using Metasploit.



# Files

* `CVE-2021-2982.py` - this offers a one-shot capability to run a single command