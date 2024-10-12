CVE-2022-10270
影响版本：
向日葵个人版 Windows <= 11.0.0.33
向日葵简约版 <= V1.0.1.43315（2021.12）

thread_port_scan.py多线程扫描工具
eg：python thread_port_scan.py --ip <ip> --port <port list> --thread <num>     #参数需使用者指定
       python thread_port_scan.py                                                  #均使用默认参数
--ip 需要扫描的ip地址   默认扫描ip地址为：127.0.0.1
--port 需要扫描的端口列表  默认扫描端口为：<40000,65535>
--thread 扫描时的线程数  默认线程数为100

--help 帮助




sunflower_poc_exp.py 漏洞验证及扫描工具

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



根据需求安装第三方库
