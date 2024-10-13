CVE-2018-16987
==============

This is a cleartext storage of sensitive information & sensitive information exposure vulnerability I found in Squash TM during a penetration test.

SquashTM
--------
Squash TM is a web interface used to manage test cases. [Link to the project](https://www.squashtest.org/en)

Description
-----------
Squash TM through at least 1.18.0 presents the cleartext passwords of external services in the administration panel, as demonstrated by a ta-server-password field in the HTML source code.

Details
-------
In SquashTM's administration panel, the external services (a.k.a. automation servers) page contain the cleartext password of the service's account. These external services could be anything but a popular example is a Jenkins server.

Here's an example URL: http://localhost:8080/squash/administration/test-automation-servers/1

Here's an extract of the page's source code:
```html
      <label for="ta-server-password">Password</label>
      <div id="ta-server-password" class="display-table-cell" style="font-weight: bold;">cleartext_password</div>
```

For this to happen, it also means that passwords of external services are stored as cleartext, which I confirmed by grepping the password against the database (H2 and postgresql).

Also, this vulnerability is heightened by the fact that the application defaults are:
* admin/admin credentials
* HTTP unencrypted communications

Suggested Scoring
-----------------
* Attack vector: network
* Attack complexity: low
* Authentication required: yes (admin)
* Impacts: confidentiality

Suggested scoring: 4.1 (CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:N/A:N)

Timeline
--------
* 2018-07-20: Vulnerability reported as a [private security bug](https://ci.squashtest.org/mantis/view.php?id=7553)
* 2018-09-11: ACK required from editor
* 2018-09-13: Disclosure to the community ([oss-security](https://www.openwall.com/lists/oss-security/2018/09/13/1) and [Mitre](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2018-16987))

Further work
------------
Just as an FYI for future researchers, passwords of actual users are stored as SHA1. Not ideal.
I briefly audited the codebase, seems like all SQL requests are correctly built (prepared statements).
There are some deserializations (report generation and search function) from unfiltered user input (GET parameters) using a vulnerable version of the Jackson component but they don't seem exploitable because [there is no polymorphic type handling](https://medium.com/@cowtowncoder/on-jackson-cves-dont-panic-here-is-what-you-need-to-know-54cd0d6e8062).
