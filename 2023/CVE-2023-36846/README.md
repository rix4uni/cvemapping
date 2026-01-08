## Remote Code Execution in Juniper JunOS (SRX and EX Series) - CVE-2023-36846 Exploit

### Description

This exploit targets a Missing Authentication for Critical Function vulnerability present in Juniper Networks Junos OS on SRX Series. The vulnerability permits an unauthenticated, network-based attacker to cause limited impact to the file system integrity. By sending a specific request that doesn't mandate authentication, an attacker can upload arbitrary files via J-Web, leading to a loss of integrity for a certain portion of the file system. This can potentially be chained to other vulnerabilities. 

Further details can be found on [BleepingComputer](https://www.bleepingcomputer.com/news/security/exploit-released-for-juniper-firewall-bugs-allowing-rce-attacks/).

**Affected Versions**: 
- All versions prior to 20.4R3-S8
- 21.2 versions prior to 21.2R3-S6
- 21.3 versions prior to 21.3R3-S5
- 21.4 versions prior to 21.4R3-S5
- 22.1 versions prior to 22.1R3-S3
- 22.2 versions prior to 22.2R3-S2
- 22.3 versions prior to 22.3R2-S2, 22.3R3
- 22.4 versions prior to 22.4R2-S1, 22.4R3

### Usage

To use the exploit, you can either target a single URL or multiple URLs from an input file. Here's how:

**Single URL Targeting**:
```bash
$ python3.10 exploit.py --url https://example.com
```

**Multiple URLs from Input File**:
```bash
$ python3.10 exploit.py --file path_to_urls.txt --output path_to_output.txt
```

Additional options:
```bash
-h, --help            Show this help message and exit.
-t THREADS, --threads THREADS
                      Specify the number of threads for concurrent scanning.
-o OUTPUT, --output OUTPUT
                      Specify the output file to store results.
```

Run the following command to view all available options:
```bash
$ python3.10 exploit.py -h
```

### Mitigations

It is advised to update to the latest version of JunOS or apply patches made available by Juniper. If these actions are not achievable, consider the workaround provided by Juniper on their support portal.
