# CVE-2023-51764
Postfix SMTP Smuggling - Expect Script POC

send an email that is legitimate, but inside the email there is many others emails (different senders, recipients, subjet, etc).
The initial email is check for SPF/DKIM/DMARC, the others inside are not !

usage: ./cve-2023-51764.sh mx.fqdn port
<br>./cve-2023-51764.sh mail.mydomain.com 25

![image](https://github.com/duy-31/CVE-2023-51764/assets/20819326/e6a0175f-b5ed-4022-aa06-386599984df3)


notes:
chmod +x cve-2023-51764.sh
<br> require app expect
<br> require legitimate ip sender and email sender (to pass SPF, DKIM, DMARC)

result:

![image](https://github.com/duy-31/CVE-2023-51764/assets/20819326/82d31732-8548-493c-98e8-28cadc571107)


------

Kudos: https://sec-consult.com/blog/detail/smtp-smuggling-spoofing-e-mails-worldwide
<br>Workaround/Fix: https://www.postfix.org/smtp-smuggling.html

------

more about me ;) https://www.linkedin.com/in/duy-huan-bui/

⚠️ Disclaimer:
IMPORTANT: This script is provided for educational, ethical testing, and lawful use ONLY. Do not use it on any system or network without explicit permission. Unauthorized access to computer systems and networks is illegal, and users caught performing unauthorized activities are subject to legal actions. The author is NOT responsible for any damage caused by the misuse of this script.

