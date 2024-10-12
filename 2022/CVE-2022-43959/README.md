# CVE-2022-43959

Bitrix Vulnerability CVE-2022-43959

## Description

Insufficiently Protected Credentials in the AD/LDAP server settings in 1C-Bitrix Bitrix24 AD/LDAP connector module before version 23.100.0 allow remote administrators to discover an AD/LDAP administrative password by reading the source code of /bitrix/admin/ldap_server_edit.php.

### CVSS

| Level | Score | CVSS | Link |
| ---      | ---       | ---       | ---       |
| Medium | 4.9 | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N | [link](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator?vector=AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N&version=3.1) |

## Steps to reproduce:
1. Get access to the Bitrix24 administrative panel.
2. Go to the AD/LDAP settings item in the Administration section.
3. Enter the AD/LDAP server settings from the list of servers.
4. Go to the Server tab.
5. Make sure that the password of the user with read access rights to the AD/LDAP server tree is masked in the “Password” line.

<img src="/password-view.png">

6. Use the browser developer tools to view the source code of the bitrix/admin/ldap_server_edit.php page.
7. Make sure that the password of the user with read access rights to the AD/LDAP server tree is displayed in clear text in the source code.

<img src="/password.png">

## Reference
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-43959

https://www.bitrix24.com/prices/self-hosted.php

https://www.bitrix24.com/security/

https://www.bitrix24.com/features/box/box-versions.php?module=ldap

## Authors

Sergey Avdeev, Dmitry Lymbin ([@lymbin](https://github.com/lymbin)) at Secware
