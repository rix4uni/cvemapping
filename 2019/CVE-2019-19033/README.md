# CVE-2019-19033: Jalios JCMS 10 Backdoor Account / Authentication Bypass

I. VULNERABILITY
-------------------------
Jalios JCMS 10 allows attackers to access any part of the website and the WebDAV server with administrative privileges via a backdoor account using any username and a specific password.


II. CVE REFERENCE
-------------------------
CVE-2019-19033


III. VENDOR
-------------------------
Jalios (https://www.jalios.com/jcms/j_6/en/home)


IV. TIMELINE
-------------------------
08/11/19 - Vulnerability discovered

09/11/19 - Vendor contacted

14/11/19 - Vendor fixes the vulnerability


V. DESCRIPTION
-------------------------
The "webdav" folder uses HTTP authentication which can be bypassed using the backdoor account. This allows to get access to the website as the administrator and then create more administrator users, change passwords of any username, delete usernames, create groups, download the list of all the users (with email addresses, phone numbers, full names ...). It is also possible to upload or overwrite any file in the WebDAV server. The "webdav" folder is located by default in the root of the website. This is caused by a vulnerable version of the "DevTools" plugin, installed by default.


VI. IMPACT
-------------------------

9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)


VII. SOLUTION
-------------------------
Possible solutions:
- Disable the DevToolsAuthenticationHandler
- Disable or uninstall the DevTools plugin.
- Upgrade DevTools plugin to version 7.1 or 8.1


VIII. REFERENCES
-------------------------
- CVE page: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-19033

- NIST page: https://nvd.nist.gov/vuln/detail/CVE-2019-19033

- Public disclosure: https://packetstormsecurity.com/files/155419/Jalios-JCMS-10-Backdoor-Account-Authentication-Bypass.html

- Jalios public issue: https://issues.jalios.com/browse/DTP-58

