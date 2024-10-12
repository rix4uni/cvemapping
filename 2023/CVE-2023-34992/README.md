# CVE-2023-34992: Fortinet FortiSIEM Unauthenticated Command Injection
Proof of concept exploit to blindly execute commands as root on vulnerable FortiSIEM appliances

## Blog Post
Root cause and indicators of compromise here:
[https://www.horizon3.ai/attack-research/disclosures/cve-2023-34992-fortinet-fortisiem-command-injection-deep-dive](https://www.horizon3.ai/attack-research/disclosures/cve-2023-34992-fortinet-fortisiem-command-injection-deep-dive/)

## Usage
```
% python3 CVE-2023-34992.py -h
usage: CVE-2023-34992.py [-h] -t TARGET [-p PORT] -c COMMAND

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        The IP address of the target
  -p PORT, --port PORT  The port of the Phoenix Monitor service
  -c COMMAND, --command COMMAND
                        The command to blindly execute 
```

## Follow the Horizon3.ai Attack Team on Twitter for the latest security research:
*  [Horizon3 Attack Team](https://twitter.com/Horizon3Attack)
*  [James Horseman](https://twitter.com/JamesHorseman2)
*  [Zach Hanley](https://twitter.com/hacks_zach)

## Disclaimer
This software has been created purely for the purposes of academic research and for the development of effective defensive techniques, and is not intended to be used to attack systems except where explicitly authorized. Project maintainers are not responsible or liable for misuse of the software. Use responsibly.
