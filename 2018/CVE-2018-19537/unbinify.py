#!/usr/bin/python2

from __future__ import with_statement
from hashlib import md5
import pyDes
import os
import sys

def undesify(filename, outputfile):
    key = '478DA50BF9E3D2CF' # Hardcoded in httpd binary
    desifier = pyDes.des(key.decode("hex"), pyDes.ECB, pad="\x00")
    with open(filename,'r') as f:
        content = f.read()
    with open(outputfile,'w') as f2:
        f2.write(desifier.decrypt(content))

def removesum(ifile, outputfile):
    with open(ifile,'r') as f:
        f.seek(16)
        data = f.read()
    with open(outputfile,'w') as f2:
        f2.write(data)

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Usage: binify.py <encrypted config file> <output file>"
        quit()
    undesify(sys.argv[1], 'tmp')
    removesum('tmp', sys.argv[2])
    os.remove('tmp')
