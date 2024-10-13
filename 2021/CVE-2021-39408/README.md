# CVE-2021-39408
A reflected Cross Site Scripting (XSS) vulnerability exists in multiple version 1.0 of the Online Student Rate System application that allows for arbitrary execution of JavaScript commands.

## Vulnerable Page
On `index.php`, the `page` parameter is vulnerable, allowing an attacker to include any javascript within script tags:

```http://localhost/index.php?page=<script>alert('test');</script>```

Discovered by Stefan Dorresteijn, August 2021
