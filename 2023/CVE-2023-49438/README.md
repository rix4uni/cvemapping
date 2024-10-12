# CVE-2023-49438

## Proof of Concept

![flask-security-too-open-redirect](https://github.com/brandon-t-elliott/CVE-2023-49438/assets/126433368/e0f0383b-bc74-43fb-a5e0-de5901a447fd)

## Description

An open redirect vulnerability in the python package [Flask-Security-Too](https://github.com/Flask-Middleware/flask-security/) <=version 5.3.2 allows attackers to redirect unsuspecting users to malicious sites via a crafted URL by abusing the ?next parameter on the /login and /register routes.

## Background

Flask-Security-Too contains logic to validate that the URL specified within the next parameter is either relative or has the same network location as the requesting URL. This is in place in an attempt to prevent open redirections.

The Flask-Security-Too python package was [previously found to be vulnerable](https://www.cve.org/CVERecord?id=CVE-2021-32618) to a bypass of the validation logic in place, and version 4.1.0 patched the previously known examples such as `https://example/login?next=\\\github.com`

However, a workaround has been discovered due to how web browsers normalize slashes in URLs, which makes the package vulnerable through version <=5.3.2.

## Examples

`https://example/login?next=/\github.com`

`https://example/login?next=\/github.com`

## Impact

It was previously noted in [CVE-2021-32618](https://www.cve.org/CVERecord?id=CVE-2021-32618) that "if Werkzeug is used (which is very common with Flask applications) as the WSGI layer, it by default ALWAYS ensures that the Location header is absolute - thus making this attack vector mute."

**However**, with Werkzeug >=2.1.0 the autocorrect_location_header configuration was changed to False - which means that location headers in redirects are relative by default. Thus, this issue may impact applications that were previously not impacted, if they are using Werkzeug >=2.1.0 as the WSGI layer.

## Mitigations

1. Update to Flask-Security-Too 5.3.3

```
pip install -U Flask-Security-Too
```

OR

2. Add these configuration options to your app (mitigates all *currently known* examples):
```
app.config['SECURITY_REDIRECT_VALIDATE_MODE'] = "regex"
app.config['SECURITY_REDIRECT_VALIDATE_RE'] = r"^/{4,}|\\{3,}|[\s\000-\037][/\\]{2,}(?![/\\])|[/\\]([^/\\]|/[^/\\])*[/\\].*"
```

OR

3. If Werkzeug >=2.1.0 is used, manually ensure autocorrect_location_header is set to True:
```
@app.after_request
def fix_location_header(response):
    response.autocorrect_location_header = True

    return response
```

## CVE Reference

[https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-49438](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-49438)

[https://nvd.nist.gov/vuln/detail/CVE-2023-49438](https://nvd.nist.gov/vuln/detail/CVE-2023-49438)

## Credit

Workaround discovered by [Brandon T. Elliott](https://www.linkedin.com/in/brandon-t-elliott/), November 2023
