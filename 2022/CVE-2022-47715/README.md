# CVE-2022-47715

Cookie missing secure flag
In Last Yard 22.09.8-1, the cookie can be stolen via via unencrypted traffic.

Sample HTTP Response:

> [Additional Information]
> HTTP/2 200 OK
> Date: x, x x 2022 04:29:43 GMT
> Content-Type: text/html; charset=utf-8
> Server: nginx
> X-Frame-Options: DENY
> Vary: Cookie
>
> Set-Cookie: LastYardVersion=22.09.8-1; expires=Sat, x x 2023 04:29:43 GMT; Max-Age=31536000; Path=/.  <----------------
>
> Set-Cookie: csrftoken=TmSZIwAxuul6kpXWDYlZ96FnNs6HTT1nNFsfkMrUMYq3mekiXv1FjqSUI2TugG74; expires=Fri, x x 2023 04:29:43 GMT; Max-Age=31449600; Path=/; SameSite=Lax; Secure
> X-Request-Id: x
