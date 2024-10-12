# CVE-2024-40324

## Description

A CRLF injection vulnerability in E-Staff v5.1 allows attackers to insert Carriage Return (CR) and Line Feed (LF) characters into input fields, leading to HTTP response splitting and header manipulation.

## Vulnerability Type

CRLF

## Vendor of Product

E-Staff

## Affected Product Code Base

E-Staff 5.1 

## Affected Component

HTTP headers

## Attack Type

Remote

## Impact Code execution

Potential for arbitrary header injection, cache poisoning, and session hijacking, cross-site scripting (XSS),  and other exploits.

## Discoverer

- Aleksey Vistorobskiy

## Attack Vectors

An attacker can insert CRLF characters into input fields, manipulating HTTP headers. For example, injecting CRLF into HTTP headers can result in HTTP response splitting


Screenshot:
![](/1.png)

## Reference

- https://e-staff.ru/estaff_home
- https://github.com/aleksey-vi/CVE-2024-40324
