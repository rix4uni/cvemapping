# Lanproxy 目录遍历漏洞 CVE-2021-3019

## 漏洞描述

Lanproxy是一个将局域网个人电脑、服务器代理到公网的内网穿透工具，支持tcp流量转发，可支持任何tcp上层协议（访问内网网站、本地支付接口调试、ssh访问、远程桌面等等）本次Lanproxy 路径遍历漏洞 (CVE-2021-3019)通过../绕过读取任意文件。该漏洞允许目录遍历读取/../conf/config.properties来获取到内部网连接的凭据。

## 漏洞影响

Lanproxy 0.1

## 网络测绘

header= "Server: LPS-0.1"

## 漏洞复现

![}TJXP1GP@NI2TWQ21HC`7N6](https://github.com/a1665454764/CVE-2021-3019/assets/143511005/1804d8e9-5a17-4de0-90ae-7a7acf1e8364)
![5E45A5 FUD~7PK9ASU_80HV](https://github.com/a1665454764/CVE-2021-3019/assets/143511005/98b80153-c27b-4777-b558-dc861c34efbd)
