# DoS WP-Cron - CVE-2023-22622 Exploit PoC

## Overview

This repository contains a script that exploits the CVE-2023-22622 vulnerability in WordPress, causing a Denial of Service (DoS) via WP-Cron. This script can be used to flood a vulnerable WordPress site with requests, potentially leading to server overload.

## Exploit Details

- **Exploit Title:** DoS WP-Cron - CVE-2023-22622
- **Date:** 07/29/2024
- **Exploit Author:** Michael Fry
- **Vendor Homepage:** [WordPress](https://wordpress.org/)
- **Software Link:** [Download WordPress](https://wordpress.org/download/)
- **Version:** Up to (including) 6.6.1
- **Tested on:** Kali Linux
- **CVE:** [CVE-2023-22622](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-22622)

## Requirements

- Python 3.x
- `requests` library
- A vulnerable instance of WordPress

## Installation

Clone the repository:

```bash
git clone https://github.com/michael-david-fry/DoS-WP-Cron-CVE-2023-22622.git
cd DoS-WP-Cron-CVE-2023-22622
```

Install the required Python libraries:

```bash
pip install requests
```

## Usage

This script allows you to send a large number of HTTP requests to a specified URL, which can potentially cause a Denial of Service (DoS) on a vulnerable WordPress site.

### Command-Line Arguments

- `-m, --method`: Specify the HTTP request method (GET or POST).
- `-u, --url`: Specify the target URL.
- `-d, --data`: Data payload for POST requests (optional).
- `-t, --threads`: Number of threads to be used (default: 500).

### Example Usage

```bash
python exploit.py -m GET -u http://example.com/wp-cron.php -t 1000
```

## Script Details

### Global Variables

- `request_counter`: Keeps track of the number of requests sent.
- `printed_msgs`: Stores messages that have been printed to avoid duplication.
- `lock`: Threading lock to ensure thread safety.

### Functions

- `print_msg(msg)`: Prints a message once.
- `handle_status_codes(status_code)`: Handles HTTP status codes and prints appropriate messages.
- `send_request(method, url, payload=None)`: Sends an HTTP request and handles the response.
- `main()`: Parses command-line arguments and initiates the sending of requests using a thread pool.

## Disclaimer

This exploit is provided for educational purposes only. The author is not responsible for any damage caused by the use of this exploit. Use it at your own risk and ensure you have proper authorization before testing it on any site.
