# CVE-2021-46704-POC
CVE-2021-46704 GenieACS Command Injection POC

Affecting genieacs package, versions >=1.2.0 <1.2.8 

# How to fix?

Upgrade genieacs to version 1.2.8 or higher.

Affected versions of this package are vulnerable to Command Injection via the ping host argument (lib/ui/api.ts and lib/ping.ts) which stems from insufficient input validation combined with a missing authorization check.
