#!/usr/bin/env python3
# CVE-2025-54068 Livewire Scanner
# Coded by Persephrak CyberSecurity Team
# Scans URLs for Livewire v3 vulnerability indicators

import requests
import re
from urllib.parse import urljoin, urlparse
import sys
from concurrent.futures import ThreadPoolExecutor

def check_livewire_vuln(url):
    """Check if site uses vulnerable Livewire v3.x"""
    try:
        # Common Livewire endpoints and fingerprints
        paths = ['/livewire/livewire.js', '/livewire/message', '/livewire/components']
        headers = {'User-Agent': 'Mozilla/5.0 (scanner)'}
        
        for path in paths:
            test_url = urljoin(url, path)
            resp = requests.get(test_url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                # Check for vulnerable Livewire version in JS or response
                if 'livewire' in resp.text.lower():
                    # Look for version pattern in JS file
                    version_match = re.search(r'v?3\.([0-6]\.[0-3])', resp.text)
                    if version_match:
                        return True, f"Vulnerable Livewire v3.{version_match.group(1)} detected"
                    
                    # Generic Livewire v3 fingerprint
                    if re.search(r'livewire.*3\.', resp.text, re.IGNORECASE):
                        return True, "Livewire v3 detected - likely vulnerable"
                        
        # Check main page for Livewire fingerprints
        resp = requests.get(url, headers=headers, timeout=10)
        if 'livewire' in resp.text.lower() and re.search(r'wire:', resp.text):
            return True, "Livewire components detected - potential vuln"
            
    except:
        pass
    return False, "No vulnerability indicators found"

def scan_file(input_file, vuln_file, safe_file, max_workers=10):
    """Main scanner function"""
    try:
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        sys.exit(1)
    
    vuln_list = []
    safe_list = []
    
    print(f"🛡️ Persephrak CyberSecurity Team - CVE-2025-54068 Scanner")
    print(f"Scanning {len(urls)} websites...\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(check_livewire_vuln, urls)
    
    for url, (is_vuln, reason) in zip(urls, results):
        status = "🚨 VULNERABLE" if is_vuln else "✅ SAFE"
        print(f"{status}: {url} - {reason}")
        
        if is_vuln:
            vuln_list.append(url)
        else:
            safe_list.append(url)
    
    # Write results
    with open(vuln_file, 'w') as f:
        f.write("# CVE-2025-54068 VULNERABLE SITES\n")
        f.write("# Upgrade Livewire to v3.6.4+\n")
        for url in vuln_list:
            f.write(url + '\n')
    
    with open(safe_file, 'w') as f:
        f.write("# CVE-2025-54068 SAFE SITES\n")
        for url in safe_list:
            f.write(url + '\n')
    
    print(f"\n✅ Results:")
    print(f"   Vulnerable: {len(vuln_list)} → {vuln_file}")
    print(f"   Safe: {len(safe_list)} → {safe_file}")
    print("\n⚠️  NOTE: False positives possible. Manual verification recommended.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scanner.py websites.txt vuln.txt safe.txt")
        sys.exit(1)
    
    scan_file(sys.argv[1], sys.argv[2], sys.argv[3])
