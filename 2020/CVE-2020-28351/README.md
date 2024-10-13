# ShoreTel 19.46.1802.0 Reflected Cross Site Scripting Attack

The conferencing component on Mitel ShoreTel 19.46.1802.0 devices could allow an unauthenticated attacker to conduct a reflected cross-site scripting attack (XSS) via the PATH_INFO to index.php, due to insufficient validation for the time_zone object in the HOME_MEETING& page.

Vulnerable payload
/index.php/%22%20onmouseover=alert(document.domain)%20?page=HOME

Vulnerability is in the HOME_MEETINGS& page, where a time_zone dropdown object is located.  Upon executing the payload, the exploit executes when the mouse is rolled over the dropdown menu object.

Discovered by Joe Helle, November 2020.  CVE issued 11/8/2020.

See the CVE listed here: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-28351
