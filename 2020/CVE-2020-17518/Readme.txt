Apache Flink目录遍历漏洞，可通过REST API读/写远程文件
漏洞编号：
CVE-2020-17518

漏洞描述：
CVE-2020-17518：通过REST API写入远程文件

受影响的版本：
Flink 1.5.1-1.11.2

安全版本：
Flink 1.11.3或Flink 1.12.0

Flink 1.5.1引入了REST API，可通过恶意修改的HTTP HEADER，将任意文件复制到文件系统的任意位置。

用法：
单个：python CVE-2020-17518.py -u http://IP:port
批量：python CVE-2020-17518.py -f url.txt