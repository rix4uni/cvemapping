# Ivanti EPM Coercion Vulnerabilities
Proof of concept exploits for Ivanti EPM CVE-2024-13159 and others which allows for unauthenticated coercion of the Ivanti EPM machine credential for use in relay attacks.

## Blog Post
Deep-dive analysis here:
[https://www.horizon3.ai/attack-research/attack-blogs/ivanti-endpoint-manager-multiple-credential-coercion-vulnerabilities/](https://www.horizon3.ai/attack-research/attack-blogs/ivanti-endpoint-manager-multiple-credential-coercion-vulnerabilities/)

## Usage
```
% python3 CVE-2024-13159.py -h
usage: CVE-2024-13159.py [-h] -u URL -t TARGET

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     The base URL of the target
  -t TARGET, --target TARGET
                        The target IP to reach out to
```

## Follow the Horizon3.ai Attack Team on Twitter for the latest security research:
*  [Horizon3 Attack Team](https://twitter.com/Horizon3Attack)
*  [James Horseman](https://twitter.com/JamesHorseman2)
*  [Zach Hanley](https://twitter.com/hacks_zach)

## Disclaimer
This software has been created purely for the purposes of academic research and for the development of effective defensive techniques, and is not intended to be used to attack systems except where explicitly authorized. Project maintainers are not responsible or liable for misuse of the software. Use responsibly.

