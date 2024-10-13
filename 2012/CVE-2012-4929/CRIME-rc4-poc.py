'''
    CRIME attack - PoC
    Implementation of the compression oracle attack behind CRIME
    Algo: RC4
    Author: mpgn <martial.puygrenier@gmail.com> - 2018
    @mpgn_x64
'''

import zlib
import random
import string
import sys
from Crypto.Cipher import ARC4

"""
    cipher = RC4(plaintext)
    KEY is random
    there is no handshake (no need)
"""

# cipher a message
def encrypt(msg):
    data = msg
    cipher = ARC4.new(KEY)
    return cipher.encrypt( zlib.compress(data) )

# decipher a message
def decrypt(enc):
    decipher = ARC4.new(KEY)
    return decipher.decrypt( zlib.decompress(enc) )

def two_tries_recursive(found, p):
    tmp = []
    for i in range(33,127):
        rand1 = ''.join(random.sample(string.ascii_lowercase + string.digits, k=17))
        rand2 = ''.join(random.sample(string.ascii_lowercase + string.digits, k=17))
        payload = rand1 + IKNOW + ''.join(found) + chr(i) + '~#:/[|/ç' + ' ' + SECRET.decode() + ' ' + rand2
        enc1 = encrypt(payload.encode())
        payload = rand1 + IKNOW + ''.join(found) + '~#:/[|/ç' + chr(i) + ' ' + SECRET.decode() + ' ' + rand2
        enc2 = encrypt(payload.encode())
        if len(enc1) < len(enc2):
            tmp.append(chr(i))

    for i in range(0, len(tmp)):
        t = 'temp' + str(i)
        t = list(found)
        t.append(tmp[i])
        sys.stdout.write('\r[+] flag=%s' % ''.join(t))
        p = two_tries_recursive(t,p)

    if len(tmp) == 0:
        p += 1
        print("")
    return p

def run():
    found = []
    p = two_tries_recursive(found, 0)
    print("\nFound", str(p), "possibilities of secret flag")
    return

if __name__ == '__main__':

    print("{-} CRIME Proof of Concept by @mpgn_x64\n")
    KEY = ''.join(random.sample(string.ascii_uppercase + string.digits, k=17))
    SECRET = b"flag={quokkalight_1s_th3_b3st_t34m}"
    IKNOW  = "flag="
    print("[+] Secret TOKEN :", SECRET.decode())
    print("[+] Encrypted with \033[33mRC4\033[0m")
    print("[+] Trying to decrypt with a compression oracle attacks using a \033[33mrecursive two_tries\033[0m method")
    print("")
    run()
    print("")
