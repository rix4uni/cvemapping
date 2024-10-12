import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.parse
import re
from packaging.version import parse as parse_version

def fetch_js_file(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    js_files = []

    for script in soup.find_all('script', src=True):
        src = script['src']
        if os.path.basename(src).startswith('index'):
            js_files.append(urllib.parse.urljoin(url, src))

    return js_files

def get_version(js_file):
    version_file_pattern = r'version-\w{8}\.js'
    version_pattern = r'const\s+i\s*=\s*"([^"]+)"'
    response = requests.get(js_file)
    version_file = re.search(version_file_pattern, response.text).group()
    version_file = urllib.parse.urljoin(js_file, version_file)
    response = requests.get(version_file)
    version = re.search(version_pattern, response.text).group(1)
    return version
    
def is_vulnerable(version_str, target_version_str='2.0.0-beta.9'):
    version = parse_version(version_str)
    target_version = parse_version(target_version_str)
    
    return version < target_version

def main():
    url = sys.argv[1]
    js_files = fetch_js_file(url)
    
    for js_file in js_files:
        version = get_version(js_file)
        vulnerable = is_vulnerable(version)
        print(f"[{'!' if vulnerable else '+'}] Nginx-ui version: {version} Vulnerable: {vulnerable}")

if __name__ == "__main__":
    main()
