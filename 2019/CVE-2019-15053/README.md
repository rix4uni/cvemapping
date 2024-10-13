# CVE-2019-15053
(FAB-2019-00156) Vulnerability discoverd by me CVE-2019-15053

Advisory: [advisory.txt](./advisory.txt)

## Basic Info

```
Advisory ID..........: FAB-2019-00156
Product..............: HTML Include and replace macro
Manufacturer.........: The Plugin People
Affected Version(s)..: 1.4.2 and before
Tested Version(s)....: 1.4.2
Vulnerability Type...: Cross-Site Scripting (CWE-79)
Risk Level...........: Medium
CVSS v3.0............: 6.8
Vektor String........: CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:L/A:L/E:F/RL:W
Vendor Homepage......: https://thepluginpeople.atlassian.net/
Software Link........: https://marketplace.atlassian.com/apps/4885/html-include-and-replace-macro
Solution Status......: Reported
Manufacturer Informed: 2019-08-13
Solution Date........: 2019-08-14
Public Disclosure....: 2019-08-14
CVE Reference........: CVE-2019-15053
Author of Advisory...: Francesco Emanuel Bennici, FABMation GmbH
```

## Credits

This security vulnerability was found by _Francesco Emanuel Bennici <eb@fabmation.de>_
of FABMation GmbH.


## Description

HTML Include and replace macro Plugin for Confluence Server adds the possibility
to "import" external HTML Sites within an Confluence Site.
The Plugin/ Macro provides a functionality to disable JavaScript (and/ or)
(CSS) Styles.

An attacker can prepare an HTML page to run JavaScript Code on the Confluence
even if "includeScripts" is set to `false`.

Enabling or Disabling "includeStyles" does not affect the functionality
of the Exploit


## PoC/ Exploit

A working PoC/ Exploit can be found under [`poc/`](poc/).
Upload the Files to an public available Server and include the `index.html` in
a Confluence Page (and disable JavaScript).
Now you can share the Confluence Page with (eg.) an Systemadministrator and if
he access the Site, you can Hijack/ "Copy" his Session.
