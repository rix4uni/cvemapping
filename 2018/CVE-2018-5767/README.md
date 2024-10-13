# Research and Author
- David Baker
- Article: [Sometimes Exploits Need Patches Too! Working Through a Change of Address](https://www.klogixsecurity.com/scorpion-labs-blog/sometimes-exploits-need-patches-too-working-through-a-change-of-address) (External link)

# CVE-2018-5767-AC9
An implementation of a proof-of-concept for CVE-2018-5767 (https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-5767)

    The following is an actualization of CVE-2018-5767, a vulnerability which
    exploits an unguarded call to sscanf that occurs when parsing the 'Cookie'
    header for a password. The vulnerability was initially discovered in, and
    reported for, the AC15 model router, but has been rediscovered in several
    different routers in this product line. This implementation sees it exploit the
    model AC9, which is not presently covered by any CVE. A memory address for the
    base of libc known to work on this router is 0x2ad6d000.

    See the following for more information:
    https://www.cve.org/CVERecord?id=CVE-2018-5767
    https://www.fidusinfosec.com/remote-code-execution-cve-2018-5767/
    https://www.klogixsecurity.com/scorpion-labs-blog/sometimes-exploits-need-patches-too-working-through-a-change-of-address

    usage: CVE-2018-5767-AC9.py [-h] [-t TARGET] [-p PORT] [-l LIBC] [-c COMMAND]
                                [-v] [-a]

    options:
      -h, --help            show this help message and exit
      -t TARGET, --target TARGET
                            target URL or IP address to throw against
      -p PORT, --port PORT  target port to throw against (default = 80)
      -l LIBC, --libc LIBC  estimated base address of libc (default = 0x2ad6d000)
      -c COMMAND, --command COMMAND
                            command(s) to be run on target (default = exit)
      -v, --verbose         increase output verbosity (currently not implemented)
      -a, --about           print information about this vulnerability then exit
