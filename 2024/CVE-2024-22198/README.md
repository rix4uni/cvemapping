# CVE-2024-22198 - authenticated remote code execution in Nginx-ui

## Description

This tool made for remote checking your Nginx-ui version and notify if it's vulnerable to CVE-2024-22198.

Nginx-UI is a web interface to manage Nginx configurations. It is vulnerable to arbitrary command execution by abusing the configuration settings. The `Home > Preference` page exposes a list of system settings such as `Run Mode`, `Jwt Secret`, `Node Secret` and `Terminal Start Command`. While the UI doesn't allow users to modify the `Terminal Start Command` setting, it is possible to do so by sending a request to the API. This issue may lead to authenticated remote code execution, privilege escalation, and information disclosure. This vulnerability has been patched in version 2.0.0.beta.9.

## Example

```
➜  python3 nginxui_checker.py http://172.17.0.4
[!] Nginx-ui version: 2.0.0-beta.8 Vulnerable: True
```

## Exploit

N/A

## References
 - https://nvd.nist.gov/vuln/detail/CVE-2024-22198
