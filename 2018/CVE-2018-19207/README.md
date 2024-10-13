# Exploit of Vulnerability CVE-2018-19207 in WP GDPR Compliance Plugin (WordPress)
This python script creates a user with role admin. Change the varbiables baseurl, username, email for your specific case. A working email is needed, because an email is sent to this adress in order to setup a password for the newly created user account.
It works for WP GDPR Compliance plugin in version <=1.4.2.
**Do only use this script on your own sites or when you have permission to do so (e.g. in a legal pentest).**

## Requirements
This script is written in Python 2.7. It is not tested or made to work in Python 3.

This script uses the requests package in python. It can be installed by running

```
pip install requests
```


