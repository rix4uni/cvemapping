#!/usr/bin/python2

from __future__ import with_statement
from hashlib import md5
import pyDes
import os
import sys

def md5sum(filename, buf_size=8192):
    m = md5()
    with open(filename, 'rb') as f:
        data = f.read(buf_size)
        while data:
            m.update(data)
            data = f.read(buf_size)
    return m.hexdigest()

def desify(filename, outputfile):
    key = '478DA50BF9E3D2CF' # Hardcoded in httpd binary
    desifier = pyDes.des(key.decode("hex"), pyDes.ECB, pad="\x00")
    with open(filename,'r') as f:
        content = f.read()
    with open(outputfile,'w') as f2:
        f2.write(desifier.encrypt(content))

def prependarino(originalfile, string):
    with open(originalfile,'r') as f:
        with open('tmp','w') as f2:
            f2.write(string)
            f2.write(f.read())

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Usage: binify.py <plaintext config file> <output file>"
        quit()
    sig = md5sum(sys.argv[1])
    prependarino(sys.argv[1], sig.decode("hex"))
    desify('tmp', sys.argv[2])
    os.remove('tmp')
