# Intel AMT authentication bypass example

This is a Proof-of-Concept code that demonstrates the exploitation of the __CVE-2017-5689__ vulnerability.

It is essentialy a _mitmproxy_ script that simply blanks an Authorization header "response" field.

Example usage:
```
mitmdump -p 8080 -dd --no-http2 -s blank_auth_response.py
```
