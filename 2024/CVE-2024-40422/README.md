# CVE-2024-40422

Description:
The snapshot_path parameter in the /api/get-browser-snapshot endpoint is susceptible to a path traversal attack. An attacker can manipulate the snapshot_path parameter to traverse directories and access sensitive files on the server. This can potentially lead to unauthorized access to critical system files and compromise the confidentiality and integrity of the system.

## References

+ https://github.com/stitionai/devika/pull/619
+ https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-40422
+ https://github.com/advisories/GHSA-39m5-v8xj-6c9r
