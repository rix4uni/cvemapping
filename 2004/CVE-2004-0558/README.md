This is a proof of concept exploit for CVE-2004-0558
Specific versions of CUPs (1.1.x) are vulnerable to a Denial of Service attack when sent a zero-length UDP packet
https://www.exploit-db.com/exploits/24599/

It's worth noting that this can be achieved with nmap, and this exploit was developed for research and educational purposes.


Usage:

python kill-cups.py -t 192.168.1.91


Additional command line flags were included for research purposes. UDP requires that the packet header requires an arbitrary source port.
In the exploit I have it default to 4321 but this can changed if necessary

python kill-cups.py -t 192.168.1.91 --source-port 5555
