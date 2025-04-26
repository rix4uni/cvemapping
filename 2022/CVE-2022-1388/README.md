# F5-CVE-2022-1388-Exploit
Exploit and Check Script for CVE 2022-1388


## Usage
Check against single host
```
python3 CVE-2022-1388.py -v true -u target_url
```

Attack host and test command
```
python CVE_2022_1388.py -a true -u target_url -c command 
```

Attack list of hosts
```
python CVE_2022_1388.py -s true -f file
```

masscheck.py will take a file input and check the hosts are vulnerable without exploiting them. 

## Issues
If you have an issue, create a pull request and fix it up, I'm not supporting this tool :).


### Detection:

Scanning for `/mgmt/tm/util/bash` as an endpoint, likely to be in web server logs. Or if you have a F5 go patch it, the affected versions are shown below and the patch is available here https://support.f5.com/csp/article/K23605346

### Vulnerable Versions
- BIG-IP versions 16.1.0 to 16.1.2 (Patch released)
- BIG-IP versions 15.1.0 to 15.1.5 (Patch released)
- BIG-IP versions 14.1.0 to 14.1.4 (Patch released)
- BIG-IP versions 13.1.0 to 13.1.4 (Patch released)
- BIG-IP versions 12.1.0 to 12.1.6 (End of Support)
- BIG-IP versions 11.6.1 to 11.6.5 (End of Support)
