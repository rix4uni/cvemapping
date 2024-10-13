# CVE-2021-40649

In Connx Version 6.2.0.1269 (20210623), a cookie can be issued by the application and not have the HttpOnly flag set. 

Cookie:     TSWAAuthClientSideCookie


HTTP Response:

HTTP/2 200 OK

Cache-Control: no-cache

Pragma: no-cache

Content-Type: text/xml; charset=utf-8

Expires: -1

Server: Microsoft-IIS/10.0

Set-Cookie: TSWAFeatureCheckCookie=true; path=/RDWeb/

Set-Cookie: TSWAAuthClientSideCookie=Name=test&MachineType=private&WorkSpaceID=XX; expires=Sat, 25-May-2024 06:39:35 GMT; path=/; secure

Set-Cookie: TSWAAuthHttpOnlyCookie=; expires=Mon, 11-Oct-1999 14:00:00 GMT; path=/; secure; HttpOnly

Date: Sun, 29 Aug 2021 06:39:35 GMT

Content-Length: 14764


