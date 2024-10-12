import os
import click
import argparse
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import RequestException, Timeout
from concurrent import futures

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
timeout = 30


def version_check(wordpress_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    plugin_url = f"{wordpress_url}/wp-content/plugins/royal-elementor-addons/readme.txt"
    try:
        response = requests.get(plugin_url, headers=headers, verify=False, timeout=timeout)
        if response.status_code == 200:
            content = response.text

            version_line = next((line for line in content.split('\n') if line.startswith('Stable tag:')), None)
            if version_line:
                version = version_line.split(':')[1].strip()
                if version <= '1.3.70':
                    print(f"\033[92m{wordpress_url} > [Plugin VULN]\033[0m")  # Green color
                    with open("vuln.txt", "a") as vuln_file:
                        vuln_file.write(wordpress_url + "\n")
                else:
                    print(f"\033[91m{wordpress_url} > [Plugin NOT Vuln]\033[0m")  # Red color
            else:
                print(f"\033[91m{wordpress_url} > [Failed GET version]\033[0m")  # Red color
        else:
            print(f"\033[91m{wordpress_url} > [Failed to fetch the readme.txt file]\033[0m")  # Red color
            if "add-listing" in response.text and "get-nearby-listings" in response.text:
                print(f"\033[91m{wordpress_url} > Was unable to read readme.txt but the plugin might be installed\033[0m")  # Red color
                with open("vuln.txt", "a") as vuln_file:
                    vuln_file.write(wordpress_url + "\n")
            else:
                print(f"\033[91m{wordpress_url} > [Plugin NO installed]\033[0m")  # Red color

    except (RequestException, ConnectionError, Timeout) as e:
        print(f"\033[91m{wordpress_url} > [UNKNOWN ERROR]\033[0m")  # Red color

    return False


def process_domain(domain):
    version_check(domain)


def process_domains(file_path, num_threads):
    with open(file_path, "r") as file:
        domains = file.read().splitlines()
        with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(process_domain, domains)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--file", required=True, help="Path to the file containing multiple domains")
    parser.add_argument("-t", "--threads", required=True, type=int, help="Number of threads")
    args = parser.parse_args()
    file_path = args.file
    num_threads = args.threads

    process_domains(file_path, num_threads)
