CVE-2014-0521 Adobe Reader vulnerability
========================================

This JavaScript based Adobe Reader vulnerability affects all versions of Adobe Reader on all platforms prior to version 11.0.07 (released on May 13, 2014). The bug was found by [Gábor Molnár](https://twitter.com/molnar_g) and was reported on March 10, 2014.

Advisories:
 - [CVE-2014-0521](http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0521)
 - [Adobe Security Bulletin APSB14-15](http://helpx.adobe.com/security/products/reader/apsb14-15.html)

Presentations:
 - Camp++ 2014 (English): video (soon), slides: [html](http://molnarg.github.io/cve-2014-0521/), [pdf](http://molnarg.github.io/cve-2014-0521/cve-2014-0521.pdf)
 - Ethical Hacking Conference 2014 Hungary (Hungarian): [video](https://www.youtube.com/watch?v=znLBb1e3b3E), [slides](http://molnarg.github.io/cve-2014-0521/js-buvesztrukkok-ethack2014.pdf)

Proof of Concept PDFs:
 - [cve-2014-0521-poc-1.pdf](http://molnarg.github.io/cve-2014-0521/cve-2014-0521-poc-1.pdf): Reading the C:\notes\passwords file and echoing the contents in an alert window.
 - [cve-2014-0521-poc-2.pdf](http://molnarg.github.io/cve-2014-0521/cve-2014-0521-poc-2.pdf): Reading the C:\notes\passwords file and sending the contents to a WebDAV server running on 192.168.56.1:9999 . This uses an undocumented API and is less reliable. For testing I recommend using [PyWebDAV](https://code.google.com/p/pywebdav/), a lightweight WebDAV server.
