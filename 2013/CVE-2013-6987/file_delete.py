from sys import argv
import requests
import json

#proxy = {"http": "127.0.0.1:8080"}

#authenticated user id
SynoToken  = argv[1] 
url = argv[2] + "/webapi/FileStation/file_delete.cgi"
path = argv[3]

payload = {"path"   : path,
           "method" : "start",
           "version": "1",
           "api"    : "SYNO.FileStation.Delete"
           }

if (not url.startswith("http://")):
    url = "http://" + url

r = requests.post(url, data=payload, cookies={"id" : SynoToken},
                                     headers={"X-SYNO-TOKEN" : SynoToken}) #proxies=proxy
print r.text

