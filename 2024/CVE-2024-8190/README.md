# CVE-2024-8190: Ivanti Cloud Service Appliance Authenticated Command Injection
Proof of concept to exploit CVE-2024-8190 on vulnerable devices.

## Blog Post
Root cause and indicators of compromise here:
[https://www.horizon3.ai/attack-research/cisa-kev-cve-2024-8190-ivanti-csa-command-injection/](https://www.horizon3.ai/attack-research/cisa-kev-cve-2024-8190-ivanti-csa-command-injection/)

## Usage
```
% python3 CVE-2024-8190.py -h
usage: CVE-2024-8190.py [-h] -u URL --username USERNAME --password PASSWORD -c COMMAND

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     The base URL of the target
  --username USERNAME   The application username
  --password PASSWORD   The application password
  -c COMMAND, --command COMMAND
                        The command to execute blind
```

## Follow the Horizon3.ai Attack Team on Twitter for the latest security research:
*  [Horizon3 Attack Team](https://twitter.com/Horizon3Attack)
*  [James Horseman](https://twitter.com/JamesHorseman2)
*  [Zach Hanley](https://twitter.com/hacks_zach)

## Disclaimer
This software has been created purely for the purposes of academic research and for the development of effective defensive techniques, and is not intended to be used to attack systems except where explicitly authorized. Project maintainers are not responsible or liable for misuse of the software. Use responsibly.
