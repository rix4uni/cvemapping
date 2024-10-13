PixelDump - CVE-2016-8462
=========================

PixelDump (CVE-2016-8462) was one of <redacted number> Pixel bootloader vulnerabilities found/worked out by [beaups](https://twitter.com/firewaterdevs) and [Jon 'jcase' Sawyer](https://twitter.com/jcase).


Disclaimer
----------
This is a dirty POC that was never intended to be released, I just copied another project, spent a few minutes adding a few lines, and sent it to Google to boost our bounty reward amount. Lame yes. Working(ish) yes.

Let me repeat, this is AWFUL code. Do not actually assume you can use this for anything.

Details
-------
This vulnerability allows you to effectively 'read' data off the device while in bootloader mode, even with a locked bootloader.

While many people found the vulnerability, we found it first and managed to collect $4000 for it from Google, which we donated to the Clallam County Special Olympics.
Vulnerability was also found by the [Roee Hay](https://twitter.com/roeehay) at IBM, he has a write up at https://securityresear.ch/2017/01/04/fastboot-oem-sha1sum/ if you want details. He describes it quite well.


