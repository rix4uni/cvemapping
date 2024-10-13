# nfsen-exploit
Exploit for CVE-2017-6971 remote command execution in nfsen 1.3.7.

Tested on Ubuntu, probably works on everything

Vulnerability discovered by Paul Taylor/Foregenix Ltd

**Usage:** `python exploit.py <local ip> <local port> <target ip> <path>`
This generates a root-level shell on the remote machine.
