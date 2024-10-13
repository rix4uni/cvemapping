# CVE-2019-15043 POC

## Description

Proof of concept scan to check if a Grafana server is vulnerable to CVE-2019-15043. Checks the Grafana server version number and checks to see if the snapshot API allows for unauthenticated requests. 

### CVE-2019-15043

CVE-2019-15043 is a Denial-of-service vulnerability found in the Grafana snapshots API. 

This vulnerability was fixed in versions 5.4.5 and 6.3.4.

## Requirements

Only needs the requests library.

Install with `pip3 install requests`

## Usage

```
$ ./cve-2019-15043.py -h
usage: cve-2019-15043.py [-h] [-u URL] [-c]

For checking if a Grafana instance is vunlerable to CVE-2019-15043

optional arguments:
  -h, --help           show this help message and exit
  -u URL, --url URL    URL of the target Grafana instance e.g. '-u
                       https://localhost:3000'
  -c, --check-version  Only check the Grafana versio
```

## Example Output

Checking only version number:
```
$ ./cve-2019-15043.py -u http://192.168.3.38:3000 -c
[-] Testing http://192.168.3.38:3000...
[-] Status: 200
[-] Checking for version...
[-] Grafana version appears to be: 6.3.3
[+] Version seems to indicate it might be vulnerable!
```

```
$ ./cve-2019-15043.py -u http://192.168.3.38:3000 -c
[-] Testing http://192.168.3.38:3000...
[-] Status: 200
[-] Checking for version...
[-] Grafana version appears to be: 6.3.4
[!] Version seems to indicate it's probably not vulnerable.
```

Checking if snapshot API requires authentication:
```
$ ./cve-2019-15043.py -u http://192.168.3.38:3000
[-] Testing http://192.168.3.38:3000...
[-] Status: 200
[-] Checking for version...
[-] Grafana version appears to be: 6.3.3
[+] Version seems to indicate it might be vulnerable!
[-] Checking if snapshot api requires authentiation...
[+] Snapshot endpoint doesn't seem to require authentication! Host may be vulnerable.
```

```
./cve-2019-15043.py -u http://192.168.3.38:3000
[-] Testing http://192.168.3.38:3000...
[-] Status: 200
[-] Checking for version...
[-] Grafana version appears to be: 6.3.4
[!] Version seems to indicate it's probably not vulnerable.
[-] Checking if snapshot api requires authentiation...
[!] Status: 401
[!] Snapshot endpoint requires authentication! Host not vulnerable.
```

## References
* https://grafana.com/blog/2019/08/29/grafana-5.4.5-and-6.3.4-released-with-important-security-fix/
* https://bugzilla.redhat.com/show_bug.cgi?id=1746945
