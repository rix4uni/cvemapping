This repository contains a Python script and a nuclei template designed to detect vulnerabilities in Moxa ioLogik devices, specifically focusing on the CVE-2023-5961 vulnerability. Additionally, it provides information about the vulnerability and relevant security advisories.

# Vulnerability Information
CVE ID: CVE-2023-5961

Security Advisory: Moxa Security Advisory MPSA-235250

The security advisory details a vulnerability affecting the Moxa ioLogik E1200 series web server, potentially leading to unauthorized access or other security issues.

https://www.moxa.com/en/support/product-support/security-advisory/mpsa-235250-iologik-e1200-series-web-server-vulnerability

Script Information
The Python script (CVE-2023-5961.py) in this repository allows users to interact with Moxa ioLogik E1212 devices. It provides options to fetch relay information from the device's web interface and download the configuration file /ik1212.txt.

Usage

```
python iologik_script.py [--url URL] [--conf]
```

--url: URL of the ioLogik E1212 device (default: http://localhost)
--conf: Download configuration file /ik1212.txt

Example usages:

```
python iologik_script.py --url http://192.168.1.100
python iologik_script.py --url http://192.168.1.100 --conf
```

# Nuclei Template Information
The nuclei template (moxa-iologik-detection.yaml) allows users to detect Moxa ioLogik devices based on specific HTTP responses. It checks for the presence of the title "Remote Ethernet I/O Server" and specific responses, such as a 200 OK response for /ik1212.txt or the presence of "Welcome to ioLogik Series" in the response body.

Usage

```
nuclei -update-templates && nuclei -t moxa-iologik-detection.yaml -target "http://target-url.com"
```

Replace http://target-url.com with the URL of the target Moxa ioLogik device.

# Disclaimer
This repository and its contents are provided for educational and informational purposes only. Users are solely responsible for their usage of the provided script and nuclei template. The authors of this repository disclaim any responsibility for misuse or unauthorized access to devices. Always ensure that you have appropriate authorization before interacting with any devices or systems.
