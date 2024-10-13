# CVE-2018-8062
Persistent XSS on Comtrend AR-5387un router

## Exploitation explanation:
To exploit this vulnerability, once logged into the router, a WAN service must be created

Click on "Advanced Setup", "WAN Service". "Add button", "Next"

Then insert the payload into the "Enter Service Description" field. This was used for the PoC <script>alert('xss');</script>

Then click on "Next" four times to go on through the steps and finally click on "Apply/Save"

The result of the XSS will be displayed and triggered on the WAN services page

This exploit automatize the entire process bypassing CSRF protection and allowing to set a custom XSS payload

Happy hacking :)

## Disclosure timeline:
08/03/2018: Vulnerability was discovered

10/03/2018: Reported to Mitre (https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-8062)

11/03/2018: Mitre answered, CVE number reserved

11/03/2018: Reported to Comtrend as part of responsible disclosure, they never answered

16/10/2020: Two years later, reported again to Comtrend and public disclosure 
(https://twitter.com/OscarAkaElvis/status/1317004119509471233)

18/10/2020: Exploit creation

19/10/2020: Exploit sent to exploit-db

## Related links

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-8062

https://packetstormsecurity.com/files/159618/Comtrend-AR-5387un-Cross-Site-Scripting.html

https://www.exploit-db.com/exploits/48908

https://twitter.com/OscarAkaElvis/status/1317004119509471233
