# CVE-2020-8193-Citrix-Scanner

Scanning for CVE-2020-8193 - Auth Bypass check
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-8193

Supporting Documents:
https://research.nccgroup.com/2020/07/10/rift-citrix-adc-vulnerabilities-cve-2020-8193-cve-2020-8195-and-cve-2020-8196-intelligence/
https://dmaasland.github.io/posts/citrix.html

Disclaimer:
I am not responsible for the use of this tool or any damages, DO NOT USE THIS FOR ILLEGAL PURPOSES. 
This tool was designed to scan for authorised assets to automate the check for this vulnerability on multiple citrix instances.

Introduction:

This CVE is can be chained with other CVEs found during the initial research found at: https://dmaasland.github.io/posts/citrix.html

I took this script and amended it to take out the LFI payload and allow the user to parse in a file of urls to test against. Thanks to dmaasland

Install:

git clone https://github.com/PR3R00T/CVE-2020-8193-Citrix-Scanner.git

chmod +x scanner.py

amend the urls.txt file with the urls https://XX.XX format.

python3 ./scanner.py urls.txt

