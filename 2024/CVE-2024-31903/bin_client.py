#!/usr/bin/env python

import socket
import sys

if (len(sys.argv) != 4):
    print("usage: " + sys.argv[0] + " host port <file_with_message>")
    print("")
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    with open(sys.argv[3],'rb') as infile:
        msg = infile.read()
        s.send(msg)
        answer = s.recv(1024)
        print(answer)