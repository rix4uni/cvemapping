# CVE-2021-40650

In Connx Version 6.2.0.1269 (20210623), a cookie can be issued by the application and not have the secure flag set.

The following cookie was issued by the application and does not have the secure flag set:

    .ASPXANONYMOUS
    
   
HTTP/2 200 OK

Cache-Control: public, max-age=31536000,Private

Content-Type: application/x-javascript

Expires: Mon, 29 Aug 2022 06:39:37 GMT

Last-Modified: Wed, 21 Oct 2020 00:00:00 GMT

Vary: User-Agent

Server: Microsoft-IIS/10.0

X-Aspnet-Version: 4.0.30319

Set-Cookie: .ASPXANONYMOUS=l1qR3nQ_9XioD6eKgDev-GQM46hTAcsRBEjoyPNE_60KpDusdwXa8UZn6yFX3XMbdwzMhuSFtb2g9-lIIKCucb_ThwF6h6T1MMng9G3V69Pi2lqpheYMG_lepGguEcpfvLtSOJVqqQT5IwrO6p9Nxw2; expires=Sat, 06-Nov-2021 17:19:37 GMT; path=/; HttpOnly

X-Ua-Compatible: IE=Edge

X-Frame-Options: SAMEORIGIN

Referrer-Policy: strict-origin

X-Xss-Protection: 1; mode=block

X-Content-Type-Options: nosniff

Strict-Transport-Security: max-age=31536000

Date: Sun, 29 Aug 2021 06:39:36 GMT

Content-Length: 310202
