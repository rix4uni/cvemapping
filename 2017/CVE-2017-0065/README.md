# Exploiting Edge's read:// urlhandler

## Introduction

This exploit was reported to Microsoft and I was acknowledged for doing so. The exploit has been patched on March 14th 2017 under names cve-2017-0065 and MS17-007 and will not work if related patches are applied. Sourcecode is provided for educational purposes only.

## References:

https://msrc.microsoft.com/update-guide/vulnerability/CVE-2017-0065

https://docs.microsoft.com/en-us/security-updates/securitybulletins/2017/ms17-007

https://nvd.nist.gov/vuln/detail/CVE-2017-0065

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0065


## General

This exploit requires the victim has a forged file (exploit.html) on his file system on a known file location.
Victim does not need to run it, just have it. The file can then be invoked by visiting a malicious website (malicious_server.php).

With this exploit local files may be uploaded to visited malicious websites without users consent.

## Here's how to reproduce:

    1. Edit exploit.html to have your test webservers address as the form action.
    2. Serve malicious_server.php on a PHP enabled webserver, so you can access it with: http://yourwebserver.com/malicious_server.php
    3. Place exploit.html into following folder: c:\windows\system32\drivers\etc\ (read: protocol seems picky about the file location)
    4. Navigate to http://yourwebserver.com/malicious_server.php with Edge.

## Here's what should happen:

    1. Navigating to malicious_server.php should trigger browser redirect to: read:,c:\windows\system32\drivers\etc\exploit.html
    2. exploit.html should then prompt user to click anywhere on the empty page. 
    3. After a click, exploit.html will create a window with url to: read:,c:\windows\system32\drivers\etc\hosts
    4. If window creation succeeds, contents of opened window (hosts file) will be copied to a hidden form, window will be closed and the form submitted back to malicious_server.php on your webserver
    5. malicious_server.php will display contents of the submitted file
