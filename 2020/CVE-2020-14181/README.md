# CVE-2020-14181
Poc for CVE-2020-14181

Affected versions of Atlassian Jira Server and Data Center allow an unauthenticated user to enumerate users via an Information Disclosure vulnerability in the /ViewUserHover.jspa endpoint. This vulnerability was discovered by Mikhail Klyuchnikov of Positive Technologies.

POC For CVE-2020-1481 - Jira Username Enumerator/Validator

Usage: python3 cve-2020-14181.py -u 'https://{vulnerable-url}' -w '/path/to/wordlist' -o '/path/to/outfile'
