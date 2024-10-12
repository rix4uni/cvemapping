# CVE-2023-51119
Improper Access Control on D-Link DIR-605L router

## Exploitation explanation:
Due to an incorrect access control, a takeover can be done over the admin account without any kind of authentication sending a request under special circumstances (only needs a legitimate admin to be logged in)

Actually, any router's doable action on the web configuration panel can be done including the change of the admin's password (leading into the takeover)

This exploit automatize the entire process to set any password for admin user on the router

Happy hacking :)

## Disclosure timeline:

11/12/2023: Vulnerability was discovered

12/12/2023: Reported to Mitre

20/12/2023: No answer yet from Mitre, reported to D-Link as part of responsible disclosure

22/12/2023: Vulnerability confirmed by D-Link, won't fix announcement published (https://supportannouncement.us.dlink.com/announcement/publication.aspx?name=SAP10368)

23/12/2023: Vendor's announcement link shared to Mitre

04/01/2024: Mitre assigned CVE number (https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-51119)

07/01/2024: Public disclosure (https://twitter.com/OscarAkaElvis/status/1744042753707712916)

08/01/2024: Exploit creation and PoC video created (https://twitter.com/OscarAkaElvis/status/1744452649011892566)

08/01/2024: Exploit sent to Exploit-db, no answer

21/04/2024: Exploit-db resubmission

## Related links

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-51119

https://supportannouncement.us.dlink.com/announcement/publication.aspx?name=SAP10368

https://twitter.com/OscarAkaElvis/status/1744042753707712916

https://twitter.com/OscarAkaElvis/status/1744452649011892566
