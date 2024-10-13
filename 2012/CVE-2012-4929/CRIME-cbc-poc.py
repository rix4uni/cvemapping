'''
    CRIME attack - PoC
    Implementation of the compression oracle attack behind CRIME
    Algo: AES-CBC
    Author: mpgn <martial.puygrenier@gmail.com> - 2018
    @mpgn_x64
'''

import binascii
import sys
import re
import random
import string
import zlib
import hmac, hashlib, base64
from Crypto.Cipher import AES
from Crypto import Random

"""
    Implementation of AES-256 with CBC cipher mode
    cipher = plaintext + padding
    IV and KEY are random
    there is no handshake (no need) 
"""

# padding for the CBC cipher block
def pad(s):
    return (16 - len(s) % 16) * chr((16 - len(s) - 1) % 16)

# cipher a message
def encrypt( msg):
    data = msg.encode()
    compress = zlib.compress(data)
    padding = pad(compress)
    raw = compress + padding.encode()
    cipher = AES.new(KEY, AES.MODE_CBC, IV )
    return cipher.encrypt( raw )

def two_true_recursive(found,p):
    tmp = []
    for i in range(33,127):
        enc1 = encrypt(GARB + IKNOW + ''.join(found) + chr(i) + '~#:/[|/ç' + ' ' + SECRET)
        enc2 = encrypt(GARB + IKNOW + '~#:/[|/ç' + ''.join(found) + chr(i) + ' ' + SECRET)
        if len(enc1) < len(enc2):
            tmp.append(chr(i))
    for i in range(0, len(tmp)):
        t = 'temp' + str(i)
        t = list(found)
        t.append(tmp[i])
        sys.stdout.write('\r[+] flag=%s' % ''.join(t))
        p = two_true_recursive(t,p)

    if len(tmp) == 0:
        p += 1
        print("")
    return p    

def adjust_padding():
    garb = ''
    found = []
    l = 0
    origin = encrypt(garb + IKNOW + ''.join(found) + '~#:/[|/ç' + ' ' + SECRET)
    while True:  
        enc = encrypt(garb + IKNOW + ''.join(found) + '~#:/[|/ç' + ' ' + SECRET)
        if len(enc) > len(origin):
            break
        else:
            l += 1
            garb = ''.join(random.sample(string.ascii_lowercase + string.digits, k=l))
    return garb[:-1]

def run():
    found = []
    p = two_true_recursive(found, 0)d
    print("\nFound", str(p), "possibilities of secret flag")
    return

if __name__ == '__main__':

    print("{-} CRIME Proof of Concept by @mpgn_x64\n")
    IV = Random.new().read( AES.block_size )
    KEY = Random.new().read( AES.block_size )
    SECRET = "flag={quokkalight_1s_th3_b3st_t34m}"
    IKNOW  = "flag="
    print("[+] Secret TOKEN :", SECRET)
    print("[+] Encrypted with \033[33mAES-256-CBC\033[0m")
    print("[+] Trying to decrypt with a compression oracle attacks using a \033[33mrecursive two_tries\033[0m method")
    print("")
    print("[+] Adjusting the padding to 1")
    GARB = adjust_padding()
    print("")
    run()
    print("")