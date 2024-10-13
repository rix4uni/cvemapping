#!/usr/bin/env python

import sys
import socket
import threading
import time
import re
import urllib2

#NTP Amplification vulnerability scanner
#by dani87
#usage ntpdos.py <domain or ip>  or -f <server list> or -m <url> <file>
#AUTHOR DOES NOT TAKE ANY LEGAL RESPONSIBILITY FOR DAMAGE CAUSED BY THIS PROGRAM

def vuln(server):
    ntppacket = "\x17\x00\x03\x2a" + "\x00" * 4
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(60)
    try:
        sock.sendto(ntppacket,(socket.gethostbyname(server), 123))
        datarecv = sock.recvfrom(255)
        print(datarecv)
        if str(datarecv).find("\\x48") != -1:
           print("Server is vulnerable: " + server) 
        else:
           print("Server not vulnerable: " + server)
        sock.close()
    except socket.timeout:
           print("Connection to server: " + server + " timed out")
    except socket.error as e:
           print("Socket error: " + str(e)) 

threads = []

if len(sys.argv) < 2:
   print("NTP Amplification Vulnerability Scanner by dani87")
   print("Usage: ntpscanner.py <server domain or ip>")
   print("Options: -f <server list> includes servers from file")
   print("-m <url> <file> gathers ip or domain from url into file")
   sys.exit()

elif sys.argv[1] == "-m":
     if len(sys.argv) < 4:
        print("Not enough arguments supplied")
     get_url = sys.argv[2]
     read_url = urllib2.urlopen(get_url).read()
     ip_regex = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
     find_ip = re.findall(ip_regex,read_url)
     with open(sys.argv[3], "wb") as file:
          for ip in find_ip:
              print("Adding IP: " + ip + " to file: " + sys.argv[3])
              file.write(ip + "\n")
          file.close()

elif sys.argv[1] == "-f":
     serverlist = []
     with open(sys.argv[2]) as file:
          serverlist = file.readlines()
     for i in serverlist:
         i = i.rstrip("\n")
         thread = threading.Thread(target=vuln, args=(i,))
         threads.append(thread)
         thread.start()
else:
   vuln(sys.argv[1])
