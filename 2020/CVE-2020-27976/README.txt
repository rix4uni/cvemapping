CVE-2020-27976 Exploit
osCommerce Phoenix CE <=1.0.5.4 Authenticated RCE

osCommerce Phoenix CE before 1.0.5.4 allows OS command injection
remotely. Within admin/mail.php, a form POST parameter can be passed
to the application. This affects the PHP mail function, and the
sendmail -f option.


This exploit uploads a specified payload file to the base directory
of a vulnerable Phoenix CE installation. You must use valid credentials
to the installation's admin panel for <user> and <pass>.

Usage:
./exploit.py <url> <user> <pass> <payload>
  <url>     - The URL of the Phoenix CE installation.
  <user>    - Username for the admin panel.
  <pass>    - Password for the admin panel.
  <payload> - Path to the payload file to upload.

=== USER NOTES ===
- The shell you upload will be embedded in a subject line in an email
  log file, and it may appear numerous times in the log. I've found that
  this can cause problems. So, you should end your PHP shell with a
  multiline comment (/*) instead of a closing brace (?>). This has
  produced the best results during testing.

- Newlines in the payload are replaced with spaces before upload.
==================


Sources:
https://www.tenable.com/cve/CVE-2020-27976
https://herolab.usd.de/security-advisories/usd-2020-0026/
