# CVE-2020-24765

Authentication Bypass Vulnerability in <a href="https://imind.ru/">Mind Server</a> version <= 3.13.65 allows any user to steal the self-diagnostic archive via a direct request.

CVSS v2: (AV:N/AC:L/Au:N/C:P/I:N/A:N)

CVSS v2 Score (BS): 5

CVSS v3: (AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N)

CVSS v3 Score (BS): 5.3


# Information

<b>Description:</b> Authentication Bypass Vulnerability allows any user to steal the self-diagnostic archive via a direct request https://PWND.SITE/api/rs/monitoring/rs/api/system/dump-diagnostic-info?server=127.0.0.1. The archive contains copies of the main configuration files and event logs of Mind Server portal. An attacker can exploit this issue to bypass certain security restrictions and perform unauthorized actions; this may aid in launching further attacks. 

<b>Class:</b> Design Error 

<b>Researcher:</b> Vadim Golovanov

<b>Issue date:</b> 2020-07-06 (Initial Advisory)

<b>Public release:</b> 2020-10-08

<b>Disclosure Link:</b>

<b>NIST CVE Link:</b> https://nvd.nist.gov/vuln/detail/CVE-2020-24765


# POC

<b>An example of vector:<b/> the official site of Vendor

https://vcs.imind.ru/api/rs/monitoring/rs/api/system/dump-diagnostic-info?server=127.0.0.1

# Screenshots:

![](POC_IMIND_1.png)

![](POC_IMIND_2.png)
