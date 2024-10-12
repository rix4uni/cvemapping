# CVE-2023-2825

> (Unauthenticated) Directory traversal leads to file read.

## Summary of the CVE

An issue has been discovered in GitLab CE/EE affecting only version 16.0.0. An unauthenticated malicious user can use a path traversal vulnerability to read arbitrary files on the server when an attachment exists in a public project nested within at least five groups.

## Affected Versions

- Gitlab Gitlab 16.0.0 Community Edition  
- Gitlab Gitlab 16.0.0 Enterprise Edition

## Anomalies

Unauthenticated if there already is a repo with nested groups, otherwise a account with permission to create groups is needed.

## References

- [Github POC - OccamSec, May 25 2023](https://github.com/Occamsec/CVE-2023-2825)
- [Gitlab Report - pwnie, May 20 2023](https://gitlab.com/gitlab-org/gitlab/-/issues/412371)
- [CVE-details - CVSS Score 10.0](https://www.cvedetails.com/cve/CVE-2023-2825)
