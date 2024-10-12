# CVE-2024-40617
Exploit PoC for CVE-2024-40617

## Description

See Medium publication for a detail description ([Fujitsu M2M GW1500 : From M2M to M2M2P0wn](https://medium.com/@eddy.huynh/cve-2024-40617-fujitsu-m2m-gw1500-from-m2m-to-m2m2p0wn-32c4a2b5da02))


## Usage
```
 __  __ ____            ____  ____   ___                 
|  \/  |___ \ _ __ ___ |___ \|  _ \ / _ \__      ___ __  
| |\/| | __) | '_ ` _ \  __) | |_) | | | \ \ /\ / / '_ \ 
| |  | |/ __/| | | | | |/ __/|  __/| |_| |\ V  V /| | | |
|_|  |_|_____|_| |_| |_|_____|_|    \___/  \_/\_/ |_| |_|

usage: CVE-2024-40617-PoC.py [-h] [--version] -t TARGET -p PASSWORD (-c | -e)

CVE 2024-40617 Exploit PoC

optional arguments:
  -h, --help                          show this help message and exit
  --version                           show program's version number and exit
  -t TARGET, --target TARGET          Target hostname
  -p PASSWORD, --password PASSWORD    Admin Password
  -c, --check                         Check vulnerability (Not yet implemented)
  -e, --exploit                       Exploit vulnerability
```

## References
[JVN publication](https://jvn.jp/en/jp/JVN25583987/index.html)<br>


## TODO
- [ ] Check vulnerability function


## Disclaimer
The code contained in this project is intended only for research and usage on systems where the user has explicit authorization.<br>
The author of this project is not responsible or liable for misuse of the software.<br>
Use responsibly and don't be evil

