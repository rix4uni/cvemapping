from termcolor import colored, cprint
from sys import argv
import requests
import json

def list_files(jsonfile):

    for file in jsonfile["data"]["files"]:

        user  = file["additional"]["owner"]["user"]
        group = file["additional"]["owner"]["group"]
        size  = file["additional"]["size"]
        read  = file["additional"]["perm"]["acl"]["read"]
        write = file["additional"]["perm"]["acl"]["write"]
        append = file["additional"]["perm"]["acl"]["append"]
        exec_ = file["additional"]["perm"]["acl"]["exec"]
        isdir = file["isdir"]
        path  = file["path"]

        #add some colors owo
        cpath = ""
        for x in path.split("/"):
            cpath += "" if x == "" else "/"
            if x == "..":
                cpath += x
            else:
                cpath += colored(x, "red", attrs=["bold"])

                    
        cprint("{}{}{}{}{} {:8} {}:{:10} {}".format('d' if isdir else '-', 'r' if read else '-',
                                                  'w' if write else '-', 'x' if exec_ else '-', 'a' if append else '-', size,
                                                   user, group, cpath))

#proxy = {"http" : "http://127.0.0.1:8080"}

SynoToken = argv[1] #authentication cookie
url  = argv[2] + "/webapi/FileStation/file_share.cgi"
path = argv[3] #must start with /home/

payload = {"filetype"   : "all",
           "folder_path": path,
           "api"        : "SYNO.FileStation.List",
           "method"     : "list",
           "version"    : 1,
           "additional" : "real_path,owner,perm,size",
           }

if (not url.startswith("http://")):
    url = "http://" + url

r = requests.post(url, data   =payload, 
                       cookies={"id" : SynoToken}, 
                       headers={"X-SYNO-TOKEN" : SynoToken})
                       #proxies=proxy)
data = r.json()

if (data["success"]):
    list_files(data)
else:
    print r.text


