# CVE-2020-24030

------------------------------------------

## [Description]

ForLogic Qualiex v1 and v3 has weak token expiration. This allows remote unauthenticated privilege escalation and to access sensitive data via token reuse.

------------------------------------------

## [Important Dates]

- Announcement (to Vendor): 2020-07-12
- Public disclosure date: 2020-08-31

------------------------------------------

## [Vulnerability Type]

Incorrect Access Control

------------------------------------------

## [Vendor of Product]

ForLogic

------------------------------------------

## [Affected Product Code Base]

- Qualiex - v1
- Qualiex - v3
- Other versions may be affected, especially in the same family (not tested yet)

------------------------------------------

## [Affected Component]

Qualiex

------------------------------------------

## [Attack Type]

Remote

------------------------------------------

## [Impact Escalation of Privileges]

True

------------------------------------------

## [Impact Information Disclosure]

True

------------------------------------------

## [Attack Vectors]

Weak expiration in authorization token permits reuse to gain privileges and to access sensitive data

------------------------------------------

## [Has vendor confirmed or acknowledged the vulnerability?]

True

------------------------------------------

## [Discoverer]

Mauricio Santos (R&D UnderProtection), Claudemir Nunes (R&D UnderProtection) and Hesron Hori (R&D UnderProtection)

------------------------------------------

## [Thanks to]

Forlogic - Vendor's Information Security Team who collaborated to a coordinated disclosure

------------------------------------------

## [Reference]

- https://www.underprotection.com.br
- https://forlogic.net
- https://qualiex.com
- https://github.com/underprotection/CVE-2020-24030
