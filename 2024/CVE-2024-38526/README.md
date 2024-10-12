## CVE-2024-38526 - Polyfill Scanner: 

[x] Mass Urls Scanner

The polyfill.io CDN, previously compromised to serve malicious code, has now been secured with the latest fix in pdoc 14.5.1.

## Overview

- Detect potential issues 
- Automate repetitive tasks with ease

## Features

- **High Confidence Alerts**: Detects scripts from untrusted domains.
- **Polyfill Vulnerability Detection**: Identifies potential issues with `polyfill.io`.
- **URL Scanning**: Extracts and analyzes script URLs from provided web pages.
- **Logging and Reporting**: Logs results to `scan_results.txt` with color-coded output.
- **Performance Tracking**: Provides execution time for the scan.

## Example Usage

```bash

bash pollypull.sh urls.txt

Note: The script handles URLs with both http and https protocols.
Ensure that the URLs in your urls.txt file are properly formatted.
The script will process each URL and check for vulnerabilities or untrusted domains.
```

![results](https://github.com/user-attachments/assets/4aed93a8-200e-46dd-b282-d2268ff063f4)



### References:
- [Polyfill[.]io Attack Impacts Over 380,000 ](https://thehackernews.com/2024/07/polyfillio-attack-impacts-over-380000.html)

- [Polyfill supply chain attack hits 100K+ sites](https://sansec.io/research/polyfill-supply-chain-attack )

