# CVE-2019-19547
CVE-2019-19547 POC

Symantec EDR on-prem version prior to "4.3.0" is vulnerable to an unauthenticated reflected XSS via the following URL:

```
https://@IP_EDR/r3_epmp_i/v1/dx/log<insert_xss_payload_here>
```

### Reference 
* https://support.broadcom.com/security-advisory/content/security-advisories/Symantec-Endpoint-Detection-and-Response-XSS/SYMSA1502
