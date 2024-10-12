# __CVE-2024-46627 - Incorrect access control in BECN DATAGERRY v2.2 allows attackers to > execute arbitrary commands via crafted web requests.__ #

DATAGERRY v2.2 lacks access control in the REST API for the following endpoints:

`/rest/users/<id>/settings/` (GET, POST)

`/rest/users/<id>/settings/<setting>` (DELETE, PUT)

This allows an attacker to read settings, create settings, delete settings, and update settings of any user without authentication.

__Additional information__
- To reproduce this it's possible to use the docker setup here: https://datagerry.readthedocs.io/en/latest/admin_guide/setup.html (as of 25th Sept 2024).
- It's possible to determine valid payloads from the information here: https://datagerry.readthedocs.io/en/latest/api/rest/user-management.html#settings
- See the following for repro steps with pictures: https://daly.wtf/cve-2024-46627-incorrect-access-control-in-becn-datagerry-v2-2-allows-attackers-to-execute-arbitrary-commands-via-crafted-web-requests/


__This is expected to be fixed in the next release.__

Ref: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-46627
