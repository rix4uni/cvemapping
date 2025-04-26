# Exch-CVE-2021-26855
ProxyLogon is the formally generic name for CVE-2021-26855, a vulnerability on Microsoft Exchange Server that allows an attacker bypassing the authentication and impersonating as the admin. We have also chained this bug with another post-auth arbitrary-file-write vulnerability, CVE-2021-27065, to get code execution. All affected components are vulnerable by default!

As a result, an unauthenticated attacker can execute arbitrary commands on Microsoft Exchange Server through an only opened 443 port!

## Usage:
```
python ExchangeSheller.py mail.domain.com test2@domain.com
python ExchangeSheller.py IP:443 test2@domain.com
```

## Expected Output
It'll give you a shell as system

## Note:
The exploit does not brute force the emails so you will need to know a valid email on the exchange server for this to work, there are other PoCs out there that'll try a few common ones but that's on you folks!
