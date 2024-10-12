import sys
import time
import threading
import socket
import queue
import re

class threadScan(threading.Thread):                     #创建线程类：直接创建一个Thread的子类来创建一个线程对象以实现多线程
    def __init__(self,ip,portlist,timeout):
        threading.Thread.__init__(self)
        self.ip = ip
        self.portlist = portlist
        self.timeout = timeout

    def run(self):
        while True:
            if self.portlist.empty():
                break

            ip = self.ip
            port = self.portlist.get()
            timeout = self.timeout

            try:
                s = socket.socket()
                s.settimeout(timeout)
                result = s.connect_ex((ip,port))
                if result == 0:
                    # sys.stdout.write("% 6d [OPEN]n" % port)
                    print(ip, ":", port, "is open")
            except Exception as e:
                print(e)
            finally:
                s.close()


def scan_main(ip,port_list,thread_num):
    start_time = time.time()
    threads = []
    port_queue = queue.Queue()
    timeout = 2

    for port in port_list:
        port_queue.put(port)
    for i in range(thread_num):
        threads.append(threadScan(ip,port_queue,timeout))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("耗时：",time.time()-start_time,"秒")


def port_scan():                            #获取ip、port、thread进行端口扫描
    args = sys.argv

    if "--help" in args:
        help()

    if "--ip" in args:
        if "--port" in args:
            if "--thread" in args:
                ip = get_ip()                               #参数都在
                port_list = get_port_list()
                thread_num = get_thread()
            else:
                ip = get_ip()                               #线程不在
                port_list = get_port_list()
                thread_num = 100
                print("默认线程数为：", thread_num)
        else:
            if "--thread" in args:
                ip = get_ip()                               #端口不在
                port_list = list(range(40000, 65535))
                print("默认扫描端口为：", port_list)
                thread_num = get_thread()
            else:
                ip = get_ip()                               #端口、线程不在
                port_list = list(range(40000, 65535))
                thread_num = 100
                print("默认扫描端口为：", port_list)
                print("默认线程数为：", thread_num)
    else:
        if "--port" in args:
            if "--thread" in args:
                ip = "127.0.0.1"                            #ip不在
                print("默认扫描ip为：", ip)
                port_list = get_port_list()
                thread_num = get_thread()
            else:
                ip = "127.0.0.1"                            #ip、线程不在
                print("默认扫描ip为：", ip)
                port_list = get_port_list()
                thread_num = 100
                print("默认线程数为：", thread_num)
        else:
            if "--thread" in args:
                ip = "127.0.0.1"                            #IP、端口不在
                print("默认扫描ip为：", ip)
                port_list = list(range(40000, 65535))
                print("默认扫描端口为：", port_list)
                thread_num = get_thread()

            else:
                ip = "127.0.0.1"                            #ip、端口、线程都不在
                port_list = list(range(40000, 65535))
                thread_num = 100
                print("默认扫描ip为：", ip)
                print("默认扫描端口为：", port_list)
                print("默认线程数为：", thread_num)

    scan_main(ip, port_list, thread_num)


def get_port(ports):
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


def get_ip():                                      #获取运行脚本时的信息
    args = sys.argv
    if "--ip" in args:
        ip = args[args.index("--ip") + 1]
        print("扫描ip为：", ip)
        return ip
def get_port_list():
    args = sys.argv
    if ("--port" in args):
        ports = args[args.index("--port") + 1]
        port_list = get_port(ports)
        print("扫描端口为：", port_list)
        return port_list
def get_thread():
    args = sys.argv
    if ("--thread" in args):
        thread_num = int(args[args.index("--thread") + 1])
        print("线程数为：", thread_num)
        return thread_num






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
格式：python thread_port_scan.py --ip <ip> --port <port list> --thread <num>     #参数需使用者指定
    python thread_port_scan.py                                                  #均使用默认参数
--ip 需要扫描的ip地址   默认扫描ip地址为：127.0.0.1
--port 需要扫描的端口列表  默认扫描端口为：<40000,65535>
--thread 扫描时的线程数  默认线程数为100

--help 帮助
    """
    print(help)


if __name__ == "__main__":
    logo()
    port_scan()






