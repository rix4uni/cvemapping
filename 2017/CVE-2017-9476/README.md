# CVE-2017-9476

Hidden AP with Deterministic Credentials.

## Compiling

```
    cc xhscmmac2psk.c -o xhscmmac2psk
```

## Usage

```
    ./xhscmmac2psk <valid Cable Modem mac address>
```

The algorithm has been also added to [PSKracker](https://github.com/soxrok2212/PSKracker/commit/f099690ec5fdeee74b6e8ded80812dac5a415557).

## References

- [CVE-2017-9476](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9476)
- [Bastille-18.home-security-wifi-network.txt](https://github.com/BastilleResearch/CableTap/blob/master/doc/advisories/bastille-18.home-security-wifi-network.txt)
- [DEFCON 25 whitepaper](https://github.com/BastilleResearch/CableTap/blob/master/doc/pdf/DEFCON-25-Marc-Newlin-CableTap-White-Paper.pdf)
- [DEFCON 25 slides](https://github.com/BastilleResearch/CableTap/blob/master/doc/pdf/DEFCON-25-Marc-Newlin-CableTap-Slides.pdf)