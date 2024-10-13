# Research and Author
- David Baker
- Article: [Anatomy of an IoT Exploit, from Hands-On to RCE](https://www.klogixsecurity.com/scorpion-labs-blog/anatomy-of-an-iot-exploit-from-hands-on-to-rce) (External link)

# CVE-2020-12124
An implementation of a proof-of-concept for CVE-2020-12124 (https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12124)


    The following is an actualization of CVE-2020-12124, a vulnerability which
    exploits a command injection in the Wavlink WN530H4 router in which certain
    parameters are taken from URL parameters in a web request to the
    /cgi-bin/live_api.cgi endpoint and places them on the command-line without
    first verifying that it is safe to do so. Given the large number of
    vulnerabilities reported across this company's entire product line, it is
    likely that this same vulnerability exists for other models of this company's
    routers.

    See the following for more information:
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12124
    https://www.klogixsecurity.com/scorpion-labs-blog/anatomy-of-an-iot-exploit-from-hands-on-to-rce

    usage: CVE-2020-12124-PoC.py [-h] [-t TARGET] [-p PORT] [-c COMMAND]
                                 [-i IDENTITY] [-s] [-v] [-a]

    options:
      -h, --help            show this help message and exit
      -t TARGET, --target TARGET
                            target URL or IP address to throw against
      -p PORT, --port PORT  target port to throw against
      -c COMMAND, --command COMMAND
                            command(s) to be run on target (default: 'exit')
      -i IDENTITY, --identity IDENTITY
                            dummy 'identity' GET parameter (no effect on
                            functionality)
      -s, --ssl             throw over SSL (actually not seen in use in this
                            product)
      -v, --verbose         increase output verbosity (currently not implemented)
      -a, --about           display information about this exploit then exit
