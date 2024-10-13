# CVE-2018-8097 PoC

This is a simple python Proof of Concept script demonstrating the CVE-2018-8097, affecting the PyEve library for versions < 0.7.5

## Usage

```txt
usage: cve_2018_8097.py [-h] -u URL -c COMMAND

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL (where you can use the 'where' filter), e.g. http://example.com/people
  -c COMMAND, --command COMMAND
                        System command to execute (shouldn't contain quotes)
```

## Resources
- https://www.cvedetails.com/cve/CVE-2018-8097/
- https://github.com/pyeve/eve/issues/1101
- https://github.com/pyeve/eve/commit/f8f7019ffdf9b4e05faf95e1f04e204aa4c91f98
